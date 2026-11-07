#!/usr/bin/env bash
# Builds NguoiQueTanCong.apk without the Android SDK/Gradle.
# Needs JDK 17+, python3, and these jars from Maven Central in $TOOLS:
#   android-all.jar  org.robolectric:android-all:14-robolectric-10818077 (Android 14 framework, compile only)
#   dx.jar           com.jakewharton.android.repackaged:dalvik-dx:16.0.1
#   apksig.jar       com.android.tools.build:apksig:2.3.0
# A signing keystore ($TOOLS/release.jks) is created on first run.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TOOLS="${TOOLS:?set TOOLS to the folder holding android-all.jar, dx.jar, apksig.jar}"
KS_PASS="${KS_PASS:-nguoique123}"
OUT="$HERE/build"
rm -rf "$OUT"; mkdir -p "$OUT/classes" "$OUT/assets" "$OUT/signer"

cp "$HERE/../index.html" "$OUT/assets/index.html"

javac -nowarn --release 8 -cp "$TOOLS/android-all.jar" \
  -d "$OUT/classes" $(find "$HERE/src" -name '*.java')
java -cp "$TOOLS/dx.jar" com.android.dx.command.Main --dex --min-sdk-version=24 --output="$OUT/classes.dex" "$OUT/classes"

python3 "$HERE/tools/mkapk.py" "$HERE/AndroidManifest.xml" "$HERE/res" "$OUT/assets" \
  "$OUT/classes.dex" "$OUT/unsigned.apk"

[ -f "$TOOLS/release.jks" ] || keytool -genkeypair -keystore "$TOOLS/release.jks" -storetype JKS \
  -storepass "$KS_PASS" -keypass "$KS_PASS" -alias nguoique -keyalg RSA -keysize 2048 -validity 10000 \
  -dname "CN=Nguoi Que Tan Cong"
javac -nowarn -cp "$TOOLS/apksig.jar" -d "$OUT/signer" "$HERE/tools/Sign.java"
java --add-exports java.base/sun.security.x509=ALL-UNNAMED --add-exports java.base/sun.security.pkcs=ALL-UNNAMED \
  -cp "$TOOLS/apksig.jar:$OUT/signer" Sign "$TOOLS/release.jks" "$KS_PASS" nguoique \
  "$OUT/unsigned.apk" "$OUT/NguoiQueTanCong.apk"
echo "APK: $OUT/NguoiQueTanCong.apk"
