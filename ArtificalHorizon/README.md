# Artificial Horizon

A resource-only Wear OS watch face built with Watch Face Format (WFF) version 1.
It recreates the circular dial of an aircraft attitude indicator without the
Bell & Ross case or trademark.

## Time behavior

- The complete blue/ground horizon card, pitch ladder, separator, and black
  pointer rotate clockwise as a continuous 12-hour indication.
- The pale hand is the minute hand.
- The striped hand is the seconds hand and uses native WFF
  `<Sweep frequency="15" />` for the maximum WFF v1 refresh rate.
- The red aircraft reference remains fixed while the horizon rotates beneath it.
- Ambient mode removes the filled horizon and sweep seconds hand, retaining a
  sparse monochrome hour/minute presentation.

All live watch-face graphics are WFF drawing primitives or Android
VectorDrawables. `res/drawable/preview.png` is the sole raster asset and is
used only by the system watch-face picker. Its deterministic vector source is
`artwork/preview.svg`.

## Compatibility

- WFF version 1
- Minimum SDK 33 / Wear OS 4
- Target SDK 36
- 450 × 450 scalable WFF coordinate space

The face was built, installed, and visually verified on a 456 × 456 Pixel
Watch 3 running Wear OS 7 (API 37).

## Build

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :watchface:assembleDebug :watchface:bundleRelease
```

Outputs:

- `watchface/build/outputs/apk/debug/watchface-debug.apk`
- `watchface/build/outputs/bundle/release/watchface-release.aab`

Both packages are resource-only and contain no DEX files.
