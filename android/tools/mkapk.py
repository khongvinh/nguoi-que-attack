#!/usr/bin/env python3
"""Minimal APK packer (replaces aapt2 + zipalign for this tiny project).

Encodes AndroidManifest.xml to Android binary XML, builds a resources.arsc for
PNG resources under res/<type>-<density>/<name>.png, and writes an unsigned,
4-byte aligned APK containing manifest, resources, assets and classes.dex.

usage: mkapk.py AndroidManifest.xml res_dir assets_dir classes.dex out.apk
"""
import os
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

ANDROID_NS = 'http://schemas.android.com/apk/res/android'
PKG_ID = 0x7f

# android.R.attr ids (checked against the API 34 framework) and how to encode each
ATTRS = {
    'theme': (0x01010000, 'ref'), 'label': (0x01010001, 'str'), 'icon': (0x01010002, 'ref'),
    'name': (0x01010003, 'str'), 'exported': (0x01010010, 'bool'), 'launchMode': (0x0101001d, 'enum'),
    'screenOrientation': (0x0101001e, 'enum'), 'configChanges': (0x0101001f, 'flags'),
    'minSdkVersion': (0x0101020c, 'int'), 'versionCode': (0x0101021b, 'int'),
    'versionName': (0x0101021c, 'str'), 'targetSdkVersion': (0x01010270, 'int'),
    'allowBackup': (0x01010280, 'bool'), 'hardwareAccelerated': (0x010102d3, 'bool'),
}
ENUMS = {
    'launchMode': {'standard': 0, 'singleTop': 1, 'singleTask': 2, 'singleInstance': 3},
    'screenOrientation': {'unspecified': -1, 'landscape': 0, 'portrait': 1, 'sensorLandscape': 6,
                          'sensorPortrait': 7, 'userLandscape': 11},
}
FLAGS = {'configChanges': {'keyboardHidden': 0x20, 'orientation': 0x80, 'screenLayout': 0x100,
                           'uiMode': 0x200, 'screenSize': 0x400, 'smallestScreenSize': 0x800,
                           'keyboard': 0x10, 'navigation': 0x40, 'density': 0x1000}}
FRAMEWORK_REFS = {'@android:style/Theme.Black.NoTitleBar.Fullscreen': 0x0103000a}
DENSITY = {'ldpi': 120, 'mdpi': 160, 'hdpi': 240, 'xhdpi': 320, 'xxhdpi': 480, 'xxxhdpi': 640}

T_REF, T_STR, T_DEC, T_HEX, T_BOOL = 0x01, 0x03, 0x10, 0x11, 0x12


def pad4(b):
    return b + b'\0' * (-len(b) % 4)


def string_pool(strings):
    """UTF-16 ResStringPool chunk."""
    offs, data = [], b''
    for s in strings:
        offs.append(len(data))
        u = s.encode('utf-16-le')
        n = len(u) // 2
        assert n < 0x8000
        data += struct.pack('<H', n) + u + b'\0\0'
    data = pad4(data)
    hdr = 28
    start = hdr + 4 * len(strings)
    body = b''.join(struct.pack('<I', o) for o in offs) + data
    return struct.pack('<HHIIIIII', 0x0001, hdr, hdr + len(body), len(strings), 0, 0, start, 0) + body


# ---------------------------------------------------------------- resources
def scan_res(res_dir):
    """-> {type: {name: [(density, path_in_apk, src)]}}"""
    out = {}
    for d in sorted(os.listdir(res_dir)):
        typ, _, qual = d.partition('-')
        for f in sorted(os.listdir(os.path.join(res_dir, d))):
            name, ext = os.path.splitext(f)
            assert ext == '.png', f
            apk_dir = d + ('-v4' if qual in DENSITY else '')
            out.setdefault(typ, {}).setdefault(name, []).append(
                (DENSITY.get(qual, 0), f'res/{apk_dir}/{f}', os.path.join(res_dir, d, f)))
    return out


def build_arsc(res, package):
    types = sorted(res)
    keys = sorted({k for t in types for k in res[t]})
    values, ids = [], {}
    for ti, t in enumerate(types):
        for k in sorted(res[t]):
            ids[f'@{t}/{k}'] = (PKG_ID << 24) | ((ti + 1) << 16) | sorted(res[t]).index(k)
            for _, path, _ in res[t][k]:
                values.append(path)

    chunks = b''
    for ti, t in enumerate(types):
        names = sorted(res[t])
        densities = sorted({d for n in names for d, _, _ in res[t][n]})
        spec_flags = [0x0100 if len(res[t][n]) > 1 else 0 for n in names]  # CONFIG_DENSITY
        chunks += struct.pack('<HHIBBHI', 0x0202, 16, 16 + 4 * len(names), ti + 1, 0, 0, len(names))
        chunks += b''.join(struct.pack('<I', f) for f in spec_flags)
        for dens in densities:
            config = bytearray(64)
            struct.pack_into('<I', config, 0, 64)
            struct.pack_into('<H', config, 14, dens)
            struct.pack_into('<H', config, 24, 4 if dens else 0)  # sdkVersion (aapt adds -v4)
            offsets, entries = [], b''
            for n in names:
                match = [p for d, p, _ in res[t][n] if d == dens]
                if not match:
                    offsets.append(0xFFFFFFFF)
                    continue
                offsets.append(len(entries))
                entries += struct.pack('<HHI', 8, 0, keys.index(n))
                entries += struct.pack('<HBBI', 8, 0, T_STR, values.index(match[0]))
            hsize = 20 + 64
            start = hsize + 4 * len(names)
            chunks += struct.pack('<HHIBBHII', 0x0201, hsize, start + len(entries), ti + 1, 0, 0,
                                  len(names), start) + bytes(config)
            chunks += b''.join(struct.pack('<I', o) for o in offsets) + entries

    type_pool, key_pool = string_pool(types), string_pool(keys)
    name = package.encode('utf-16-le')[:254].ljust(256, b'\0')
    phdr = 288
    pkg = struct.pack('<HHII', 0x0200, phdr, 0, PKG_ID) + name
    pkg += struct.pack('<IIIII', phdr, len(types), phdr + len(type_pool), len(keys), 0)
    pkg += type_pool + key_pool + chunks
    pkg = pkg[:4] + struct.pack('<I', len(pkg)) + pkg[8:]
    vpool = string_pool(values)
    table = struct.pack('<HHII', 0x0002, 12, 12 + len(vpool) + len(pkg), 1) + vpool + pkg
    return table, ids


# ---------------------------------------------------------------- manifest
def encode_manifest(path, res_ids):
    root = ET.parse(path).getroot()
    package = root.get('package')

    def attrs_of(el):
        out = []
        for k, v in el.attrib.items():
            if k.startswith('{'):
                ns, local = k[1:].split('}')
                assert ns == ANDROID_NS and local in ATTRS, k
                rid, kind = ATTRS[local]
                if local == 'name' and v.startswith('.'):
                    v = package + v
                out.append((ns, local, rid, kind, v))
            else:
                out.append((None, k, None, 'str', v))
        return out

    # string pool: attribute names with resource ids first, in resource-map order
    all_attrs = [a for el in root.iter() for a in attrs_of(el)]
    res_names = sorted({(a[2], a[1]) for a in all_attrs if a[2]})
    strings = [n for _, n in res_names]

    def sidx(s):
        if s not in strings:
            strings.append(s)
        return strings.index(s)

    body = []

    def node(typ, ext, line=1):
        return struct.pack('<HHIII', typ, 16, 16 + len(ext), line, 0xFFFFFFFF) + ext

    ns_ext = lambda: struct.pack('<II', sidx('android'), sidx(ANDROID_NS))
    body.append(node(0x0100, ns_ext()))

    def walk(el):
        tag = el.tag
        attrs = sorted(attrs_of(el), key=lambda a: (a[2] is None, a[2] or 0, a[1]))
        ab = b''
        for ns, local, rid, kind, v in attrs:
            raw = 0xFFFFFFFF
            if kind == 'str':
                raw = sidx(v); typ, data = T_STR, raw
            elif kind == 'int':
                typ, data = T_DEC, int(v)
            elif kind == 'bool':
                typ, data = T_BOOL, 0xFFFFFFFF if v == 'true' else 0
            elif kind == 'enum':
                typ, data = T_DEC, ENUMS[local][v] & 0xFFFFFFFF
            elif kind == 'flags':
                typ, data = T_HEX, 0
                for f in v.split('|'):
                    data |= FLAGS[local][f]
            elif kind == 'ref':
                typ, data = T_REF, FRAMEWORK_REFS.get(v) or res_ids[v]
            ab += struct.pack('<IIIHBBI', sidx(ns) if ns else 0xFFFFFFFF, sidx(local), raw, 8, 0, typ, data)
        ext = struct.pack('<IIHHHHHH', 0xFFFFFFFF, sidx(tag), 20, 20, len(attrs), 0, 0, 0) + ab
        body.append(node(0x0102, ext))
        for c in el:
            walk(c)
        body.append(node(0x0103, struct.pack('<II', 0xFFFFFFFF, sidx(tag))))

    walk(root)
    body.append(node(0x0101, ns_ext()))
    pool = string_pool(strings)
    rmap = struct.pack('<HHI', 0x0180, 8, 8 + 4 * len(res_names)) + b''.join(struct.pack('<I', r) for r, _ in res_names)
    content = pool + rmap + b''.join(body)
    return struct.pack('<HHI', 0x0003, 8, 8 + len(content)) + content, package


# ---------------------------------------------------------------- zip
def write_apk(out, files):
    """files: list of (name, bytes, stored). Stored entries are aligned to 4 bytes."""
    with zipfile.ZipFile(out, 'w') as z:
        for name, data, stored in files:
            zi = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
            if stored:
                off = z.fp.tell() + 30 + len(name.encode())
                pad = -off % 4
                if pad:
                    pad += 4  # room for the 4-byte extra-field header
                    zi.extra = struct.pack('<HH', 0xD935, pad - 4) + b'\0' * (pad - 4)
            z.writestr(zi, data)


def main(manifest, res_dir, assets_dir, dex, out):
    res = scan_res(res_dir)
    root = ET.parse(manifest).getroot()
    arsc, ids = build_arsc(res, root.get('package'))
    axml, _ = encode_manifest(manifest, ids)
    files = [('AndroidManifest.xml', axml, False), ('classes.dex', open(dex, 'rb').read(), False),
             ('resources.arsc', arsc, True)]
    for t in res.values():
        for entries in t.values():
            for _, path, src in entries:
                files.append((path, open(src, 'rb').read(), True))
    for dp, _, fs in os.walk(assets_dir):
        for f in sorted(fs):
            src = os.path.join(dp, f)
            files.append(('assets/' + os.path.relpath(src, assets_dir).replace(os.sep, '/'), open(src, 'rb').read(), False))
    write_apk(out, files)
    print('wrote', out, {k: hex(v) for k, v in ids.items()})


if __name__ == '__main__':
    main(*sys.argv[1:6])
