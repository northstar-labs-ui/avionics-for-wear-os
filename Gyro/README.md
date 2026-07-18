# Gyrocompass WFF watch face

This project packages a resource-only Wear OS watch face using Watch Face
Format (WFF) version 1. It targets Wear OS 4 / API 33 and later.

## Time mapping

- `plane_hour_hand.xml` is the hour hand. Its nose points to the current hour
  and advances continuously with the minutes.
- `minute_hand.xml` is the gray minute hand with the open white triangle tip.
- `second_hand.xml` is the thin gray second hand with a white tip. It uses WFF
  `<Sweep frequency="15" />`, the highest sweep frequency allowed by WFF v1,
  and is hidden in ambient mode.

The aircraft contour in `plane_hour_hand.xml` was converted directly from the
user-supplied SVG. Its path geometry was not redrawn; only scale, position,
fill, and outline colors were adapted for the dial.

## Vector-only artwork

The dial is composed from WFF drawing primitives, text, and Android XML
VectorDrawables. The only raster source under `res/` is `preview.png`, which is
required for the watch-face picker and explicitly permitted for this project.

The picker preview is reproducible from the live vector sources:

```powershell
$python = 'C:\Users\Henry\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $python tools\render_preview.py watchface\build\preview.svg
```

Rasterize `watchface/build/preview.svg` at 450 x 450 into
`watchface/src/main/res/drawable/preview.png` with a browser or SVG renderer.

## Device scaling

The 450 x 450 dimensions in `watchface.xml` define WFF's logical coordinate
space, not a fixed device resolution. Wear OS scales that coordinate space to
the active display. The scene begins with an opaque, full-canvas background so
the face remains full-bleed on different display sizes and shapes without
stretching or maintaining device-specific layout files.

## Build

```powershell
$env:JAVA_HOME = 'C:\Program Files\Android\Android Studio\jbr'
.\gradlew.bat :watchface:assembleDebug :watchface:assembleRelease --console=plain
```

The debug APK is written to
`watchface/build/outputs/apk/debug/watchface-debug.apk`.

## Verification performed

- Google WFF validator: valid against format version 1.
- Android `assembleDebug`, `assembleRelease`, and `lintDebug`.
- Installed and rendered on a Pixel Watch 3.
- On-device check at 16:25:35 confirmed the plane/hour, triangle/minute, and
  white-tipped second-hand positions and found no missing-resource errors.

## Google memory-estimator note

Google's current memory-footprint CLI reports Android XML VectorDrawable hand
resources as "not found," although the same resources compile and render in
the Wear OS WFF runtime. This appears to be a validator limitation for vector
drawables. A Play Store submission should be rechecked against the then-current
tooling; replacing the hands with raster images would avoid that warning but
would violate this project's vector-only requirement.
