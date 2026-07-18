# Avionics for Wear OS

Avionics for Wear OS is a collection of aviation-inspired watch faces built
with Google's resource-only Watch Face Format (WFF). Each directory is a
standalone Android Studio and Gradle project, so a watch face can be built and
installed independently from the rest of the collection.

## Watch faces

| Watch face | Project | Description                                                             | Minimum API |
| --- | --- |-------------------------------------------------------------------------| ---: |
| Altitude | [`Altitude/`](Altitude/) | Altimeter-inspired dial with date display and instrument-style hands.   | 33 |
| Artificial Horizon | [`ArtificalHorizon/`](ArtificalHorizon/) | Attitude-indicator dial whose horizon card carries the hour indication. | 33 |
| Gyrocompass | [`Gyro/`](Gyro/) | Gyrocompass dial with an aircraft-shaped hour hand.                     | 33 |
| Landing Zone | [`Helicopter/`](Helicopter/) | Helipad and helicopter display with a sweeping rotor second hand.       | 33 |
| Radar Sweep | [`Radar/`](Radar/) | Configurable radar display with aircraft time hands and a sweep effect. | 33 |
| Radiocompass | [`Radiocompass/`](Radiocompass/) | Radio-compass instrument with stylized hands.                           | 34 |
| Turn Coordinator | [`TurnCoordinator/`](TurnCoordinator/) | Turn-coordinator-inspired face with rotating discs.                     | 33 |

> The `ArtificalHorizon` directory keeps its original spelling for project
> compatibility; the watch face itself is named **Artificial Horizon**.

## Requirements

- Android Studio with its bundled JDK
- Android SDK 36
- A Wear OS 4 or newer watch for projects with minimum API 33
- A Wear OS 5 or newer watch for Radiocompass (minimum API 34)
- Android SDK Platform Tools for wireless ADB installation

## Build a watch face

Open the chosen project directory in Android Studio, or build it from that
directory. On Windows PowerShell:

```powershell
cd Radar
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :watchface:assembleDebug --console=plain
```

On macOS or Linux, use `./gradlew` instead of `./gradlew.bat`. The debug build
is created locally under `watchface/build/outputs/apk/debug/`.

For instructions on installing a prebuilt apk, see [INSTALLATION.md](INSTALLATION.md).

## Screenshots

Picker previews live with each watch face under
`watchface/src/main/res/drawable/preview.png`. Full-size device captures can be
added to [`screenshots/`](screenshots/) using that directory's naming guidance.

## Contributing and releases

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Maintainers
can use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) when preparing a GitHub
release.

## License

This collection is free software licensed under the
[GNU General Public License v3.0](LICENSE). Individual third-party assets or
notices remain subject to any terms documented alongside those assets.
