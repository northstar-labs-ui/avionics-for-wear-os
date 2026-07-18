param(
    [Parameter(Mandatory = $true)]
    [string] $InputSvg,

    [Parameter(Mandatory = $true)]
    [string] $OutputVector
)

$ErrorActionPreference = "Stop"

[xml] $source = Get-Content -LiteralPath $InputSvg -Raw
$sourcePaths = @($source.svg.path)

if ($sourcePaths.Count -lt 2) {
    throw "Expected a background path followed by filled helicopter paths."
}

$colorMap = @{
    "#101b3d" = "#FF252C2F"
    "#1b458c" = "#FF667276"
    "#1b51a0" = "#FF7C878A"
    "#7e9acd" = "#FFB5BDBE"
    "#ffffff" = "#FFE4E8E7"
}

$builder = [System.Text.StringBuilder]::new()
[void] $builder.AppendLine('<?xml version="1.0" encoding="utf-8"?>')
[void] $builder.AppendLine('<!--')
[void] $builder.AppendLine('    Converted from the user-supplied SVG. The source background and')
[void] $builder.AppendLine('    stroke-only tracing guides are intentionally excluded. The group')
[void] $builder.AppendLine('    rotates the source nose to 12 o''clock and centers its usable mast.')
[void] $builder.AppendLine('-->')
[void] $builder.AppendLine('<vector xmlns:android="http://schemas.android.com/apk/res/android"')
[void] $builder.AppendLine('    android:width="450dp"')
[void] $builder.AppendLine('    android:height="450dp"')
[void] $builder.AppendLine('    android:viewportWidth="1024"')
[void] $builder.AppendLine('    android:viewportHeight="1024">')
[void] $builder.AppendLine('    <group')
[void] $builder.AppendLine('        android:name="helicopter"')
[void] $builder.AppendLine('        android:pivotX="540"')
[void] $builder.AppendLine('        android:pivotY="510"')
[void] $builder.AppendLine('        android:rotation="-62"')
[void] $builder.AppendLine('        android:scaleX="0.78"')
[void] $builder.AppendLine('        android:scaleY="0.78"')
[void] $builder.AppendLine('        android:translateX="-28"')
[void] $builder.AppendLine('        android:translateY="2">')

# The first direct fill is a white 1024-square background. The remaining
# direct fills are the visible helicopter. SVG outline guides live in a
# separate top-level group and do not need to be rasterized into the asset.
foreach ($path in ($sourcePaths | Select-Object -Skip 1)) {
    $sourceColor = $path.fill.ToLowerInvariant()
    if (-not $colorMap.ContainsKey($sourceColor)) {
        throw "No gray mapping declared for SVG fill color $sourceColor."
    }

    $pathData = ($path.d -replace '\s+', ' ').Trim()
    [void] $builder.AppendLine('        <path')
    [void] $builder.AppendLine("            android:fillColor=`"$($colorMap[$sourceColor])`"")
    [void] $builder.AppendLine("            android:pathData=`"$pathData`" />")
}

# Keep the minute indication readable without changing the helicopter's
# silhouette: this compact white triangle extends just beyond the nose.
[void] $builder.AppendLine('        <!-- Short minute pointer aligned with the helicopter''s nose. -->')
[void] $builder.AppendLine('        <path')
[void] $builder.AppendLine('            android:fillColor="#FFFFFFFF"')
[void] $builder.AppendLine('            android:pathData="M 783.27 391.67 L 827.42 359.52 L 775.85 377.49 Z" />')

[void] $builder.AppendLine('    </group>')
[void] $builder.AppendLine('</vector>')

$resolvedOutput = [System.IO.Path]::GetFullPath($OutputVector)
$outputDirectory = [System.IO.Path]::GetDirectoryName($resolvedOutput)
if (-not [System.IO.Directory]::Exists($outputDirectory)) {
    throw "Output directory does not exist: $outputDirectory"
}

[System.IO.File]::WriteAllText(
    $resolvedOutput,
    $builder.ToString(),
    [System.Text.UTF8Encoding]::new($false)
)
