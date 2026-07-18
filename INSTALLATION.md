# Installing on Wear OS with wireless ADB

Download a prebuilt APK from this repository's GitHub Releases or build the
selected watch face locally. You can then use Android Debug Bridge (ADB) from
the Android SDK Platform Tools to install it on your own watch.

## 1. Get the APK

### Download a release APK

1. Open the repository's **Releases** page on GitHub.
2. Select the release you want and expand **Assets** if necessary.
3. Download the APK named for the watch face you want to install.
4. Save it somewhere easy to find and note its full path.

Only sideload APKs from a release and publisher you trust. If a release
provides checksums, verify the downloaded file before installing it.

### Or build a debug APK locally

From the selected project directory, run:

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :watchface:assembleDebug --console=plain
```

The APK is written to:

```text
watchface/build/outputs/apk/debug/watchface-debug.apk
```

On macOS or Linux, use `./gradlew` instead of `./gradlew.bat`.

## 2. Enable developer options on the watch

1. Open **Settings** on the watch.
2. Open **System > About > Versions**. Menu names can vary slightly by watch.
3. Tap **Build number** seven times, then enter the watch PIN if prompted.
4. Return to **Settings > Developer options**.
5. Enable **ADB debugging**.
6. Enable **Wireless debugging** or **Debug over Wi-Fi**.

Keep the Android phone or computer performing the installation and the watch
on the same Wi-Fi network. Avoid guest networks or access points that isolate
wireless clients from one another.

## 3. Option A: Install with Wear Installer 2 on an Android phone

[Wear Installer 2](https://play.google.com/store/apps/details?id=org.freepoc.wearinstaller2)
is a third-party Android app that provides a graphical interface for sending
APK files to a Wear OS watch over wireless ADB. Install it on the Android phone
paired with your watch; no companion app needs to be installed on the watch.

Before starting, download the watch-face APK to the phone, preferably into its
**Download** folder. Keep the phone and watch on the same Wi-Fi network.

1. Open Wear Installer 2 on the phone.
2. On the watch, open **Settings > Developer options > Wireless debugging**
   and note the displayed IP address.
3. Enter that IP address on the Wear Installer 2 home screen and tap **Done**.
4. If the phone has not previously been paired for wireless debugging, open
   the Wear Installer 2 menu, select **Pair with watch**, and tap **Enable**.
5. On the watch, select **Pair new device**. The watch displays a six-digit
   pairing code and a five-digit pairing port.
6. In Wear Installer 2, enter the pairing code, a space, and the pairing port,
   then tap **Done**. Wait for **Pairing successful**.
7. Return to the main Wireless debugging screen on the watch. It now shows a
   random debugging port after the IP address. Enter this port on the Wear
   Installer 2 home screen. The debugging port is different from the pairing
   port used in the previous step.
8. Select **Custom APK** in Wear Installer 2 and choose the downloaded
   watch-face APK.
9. Tap **Install** and wait for the app to report that installation completed.

If the phone is already listed under **Paired devices** on the watch, pairing
does not need to be repeated. Enter the current random debugging port shown by
the watch and proceed to **Custom APK**. Ports can change whenever wireless
debugging is restarted.

Wear Installer 2's controls may change between versions. Consult the
[official Wear Installer 2 help page](https://freepoc.org/wear-installer-2-help-page/)
if its current screens differ from the labels above.

## 4. Option B: Install with command-line ADB

### Pair and connect

Recent Wear OS versions display separate addresses and ports for pairing and
debugging. In **Wireless debugging**, choose **Pair new device** or **Pair
device with pairing code** and note the pairing address and six-digit code.

On the computer, run:

```text
adb pair WATCH_IP:PAIRING_PORT
```

Enter the pairing code when prompted. Return to the main Wireless debugging
screen, note its debugging address, and connect:

```text
adb connect WATCH_IP:DEBUG_PORT
adb devices -l
```

The pairing and debugging ports may be different and can change when wireless
debugging is restarted. Use the exact values currently shown by the watch.

On older watches that expose only **Debug over Wi-Fi**, the watch may show a
single address such as `192.168.1.25:5555`. Connect directly with:

```text
adb connect 192.168.1.25:5555
```

Approve the debugging authorization prompt on the watch if one appears.

### Install the watch face

Replace `WATCH_SERIAL` with the address shown by `adb devices` and
`PATH_TO_APK` with the full path to the downloaded or locally built APK:

```text
adb -s WATCH_SERIAL install -r "PATH_TO_APK"
```

For example, from a project directory you can install its local debug build
with:

```text
adb -s WATCH_SERIAL install -r "watchface/build/outputs/apk/debug/watchface-debug.apk"
```

`-r` replaces an existing debug installation while preserving compatible app
data. A successful installation ends with `Success`.

Open the watch-face picker by touching and holding the current watch face. The
new face should be available under **Add watch face** or the equivalent menu.

## Troubleshooting

- **Wear Installer 2 cannot connect:** recheck the current watch IP address and
  debugging port, confirm the phone and watch are on the same Wi-Fi network,
  temporarily disable a phone VPN, and restart both devices before pairing
  again.
- **Wear Installer 2 cannot find the APK:** move the file into the phone's
  **Download** folder and grant the app file access if Android requests it.
- **Wear Installer 2 pairing fails:** confirm the entry contains the six-digit
  code, one space, and the pairing port—not the later debugging port.
- **`adb` is not recognized:** add the Android SDK `platform-tools` directory
  to your command path, or run ADB by its full path.
- **Connection refused or timed out:** confirm both devices are on the same
  network, recheck the current debugging port, and disable any client-isolation
  setting on the Wi-Fi network.
- **Device is unauthorized:** revoke wireless debugging authorizations on the
  watch, then pair again and accept the watch prompt.
- **More than one device is connected:** include `-s WATCH_SERIAL` in install
  and other device commands.
- **Install reports a version or signature conflict:** uninstall the existing
  package only if you are comfortable removing that watch face's local data,
  then retry the install.

## Disconnect securely

When finished, run `adb disconnect WATCH_SERIAL`, then disable **Wireless
debugging** and **ADB debugging** on the watch. Revoke paired debugging devices
from the watch settings if the computer should no longer be trusted.
