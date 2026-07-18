# Landing Zone

Landing Zone is a branding-free, screw-free Wear OS watch face built entirely
with Watch Face Format (WFF) version 1.

## Time display

- The yellow perimeter notch is the native WFF `HourHand`.
- The helipad H is a second `HourHand`, so it rotates with the notch.
- The gray helicopter nose is the native WFF `MinuteHand`.
- The four-blade rotor is the native WFF `SecondHand` and uses
  `<Sweep frequency="SYNC_TO_DEVICE" />` for continuous motion.

All runtime artwork is vector-based. The dial uses WFF `PartDraw` primitives,
and the four moving layers are Android `VectorDrawable` resources. The only
raster resource in the watch-face package is the required picker preview PNG.

## Source layout

- `watchface/src/main/res/raw/watchface.xml` — dial, ambient behavior, and hands
- `watchface/src/main/res/drawable/hour_notch.xml` — hour indicator
- `watchface/src/main/res/drawable/hour_h.xml` — rotating helipad H
- `watchface/src/main/res/drawable/helicopter_minute.xml` — gray minute asset
- `watchface/src/main/res/drawable/rotor_second.xml` — sweep rotor
- `watchface/src/main/res/drawable/preview.png` — 450 × 450 picker preview

## Replacing the helicopter

The checked-in helicopter was converted from the supplied SVG with:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\tools\convert_helicopter_svg.ps1 `
  -InputSvg <source.svg> `
  -OutputVector .\watchface\src\main\res\drawable\helicopter_minute.xml
```

The converter removes the source's white background and stroke-only tracing
guides, maps its blue palette to layered steel grays, rotates the nose to
12 o'clock, and places the selected mast point at the 450-square dial center.

## Build

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :watchface:assembleDebug --console=plain
```

The debug APK is written to
`watchface/build/outputs/apk/debug/watchface-debug.apk`.

## Picker preview

`tools/make_picker_preview.py` turns a 456 × 456 Pixel Watch 3 screen capture
into the 450 × 450 picker PNG. It repairs only the outer 6-o'clock sector if
Wear OS overlays an ongoing-activity icon there; the rest remains the exact
device-rendered face.

## Ambient mode

Ambient mode switches to a pure-black field, hides the H, yellow landing ring,
minute rail, rotor, and rotor hub, and retains dim hour/minute indicators plus
the twelve major indices.
