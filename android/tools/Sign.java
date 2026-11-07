import com.android.apksig.ApkSigner;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.cert.X509Certificate;
import java.util.Collections;

/** Signs an APK with APK Signature Scheme v2 (minSdk 24, so no v1/JAR signature needed). Args: keystore pass alias in.apk out.apk */
public class Sign {
    public static void main(String[] a) throws Exception {
        String ks = a[0], pass = a[1], alias = a[2], in = a[3], out = a[4];
        KeyStore store = KeyStore.getInstance("JKS");
        try (InputStream is = new FileInputStream(ks)) { store.load(is, pass.toCharArray()); }
        PrivateKey key = (PrivateKey) store.getKey(alias, pass.toCharArray());
        X509Certificate cert = (X509Certificate) store.getCertificate(alias);
        ApkSigner.SignerConfig cfg =
                new ApkSigner.SignerConfig.Builder("CERT", key, Collections.singletonList(cert)).build();
        new ApkSigner.Builder(Collections.singletonList(cfg))
                .setInputApk(new File(in)).setOutputApk(new File(out))
                .setMinSdkVersion(24)
                .setV1SigningEnabled(false).setV2SigningEnabled(true)
                .build().sign();
        System.out.println("Signed " + out);
    }
}
