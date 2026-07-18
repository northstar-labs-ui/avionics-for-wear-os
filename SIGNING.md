# Release signing

All Avionics watch faces use one shared app-signing key. The private key and
its passwords must stay outside this repository.

## 1. Generate the app-signing key

Run these commands in PowerShell. `keytool` prompts for the passwords and
certificate identity, so the passwords do not enter the shell history.

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.android-keys" | Out-Null

& 'C:\Program Files\Android\Android Studio\jbr\bin\keytool.exe' `
  -genkeypair -v `
  -keystore "$env:USERPROFILE\.android-keys\avionics-release.jks" `
  -storetype JKS `
  -alias avionics `
  -keyalg RSA `
  -keysize 4096 `
  -validity 36500
```

Use a unique password-manager-generated password. Press Enter at the key
password prompt to reuse the keystore password, or record both passwords if
they differ.

## 2. Configure local release builds

Create `%USERPROFILE%\.android-keys\avionics-signing.properties` with:

```properties
storeFile=C:/Users/Henry/.android-keys/avionics-release.jks
storePassword=REPLACE_WITH_KEYSTORE_PASSWORD
keyAlias=avionics
keyPassword=REPLACE_WITH_KEY_PASSWORD
```

This file is outside the repository. Do not commit it, the keystore, or either
password. Release tasks fail instead of producing an unsigned artifact when
this file is absent.

Automated build environments can point to an equivalent temporary properties
file with the `AVIONICS_SIGNING_PROPERTIES` environment variable.

## 3. Back up the signing identity

Keep at least two encrypted backups of `avionics-release.jks` in separate
locations. Store the alias and passwords in a password manager. Losing this
private key prevents GitHub builds from updating existing installations.

## 4. Configure Google Play later

For each package, choose **Provide a copy of your app signing key** during Play
App Signing setup and transfer the `avionics` key using Google's PEPK tool.
Create a different upload key for routine `.aab` uploads; do not replace this
app-signing key with the upload key.
