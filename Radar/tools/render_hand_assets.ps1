param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase

function Convert-SvgToPng {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$Target,
        [Parameter(Mandatory = $true)][int]$PixelWidth,
        [Parameter(Mandatory = $true)][int]$PixelHeight
    )

    [xml]$document = Get-Content -Raw -LiteralPath $Source
    $viewBox = @($document.DocumentElement.GetAttribute("viewBox") -split "\s+" | ForEach-Object { [double]$_ })
    if ($viewBox.Count -ne 4) {
        throw "Expected a four-value viewBox in $Source"
    }

    $scaleX = $PixelWidth / $viewBox[2]
    $scaleY = $PixelHeight / $viewBox[3]
    $visual = [System.Windows.Media.DrawingVisual]::new()
    $drawing = $visual.RenderOpen()
    $drawing.PushTransform([System.Windows.Media.ScaleTransform]::new($scaleX, $scaleY))

    foreach ($path in $document.SelectNodes("//*[local-name()='path']")) {
        $geometry = [System.Windows.Media.Geometry]::Parse($path.GetAttribute("d"))

        $transform = $path.GetAttribute("transform")
        if ($transform) {
            if ($transform -notmatch '^matrix\(\s*([-+\d.eE]+)[,\s]+([-+\d.eE]+)[,\s]+([-+\d.eE]+)[,\s]+([-+\d.eE]+)[,\s]+([-+\d.eE]+)[,\s]+([-+\d.eE]+)\s*\)$') {
                throw "Unsupported SVG path transform '$transform' in $Source"
            }
            $matrix = [System.Windows.Media.Matrix]::new(
                [double]$Matches[1],
                [double]$Matches[2],
                [double]$Matches[3],
                [double]$Matches[4],
                [double]$Matches[5],
                [double]$Matches[6]
            )
            $geometry = $geometry.Clone()
            $geometry.Transform = [System.Windows.Media.MatrixTransform]::new($matrix)
        }

        $brush = $null
        $fill = $path.GetAttribute("fill")
        if ($fill -and $fill -ne "none") {
            $fillColor = [System.Windows.Media.ColorConverter]::ConvertFromString($fill)
            $brush = [System.Windows.Media.SolidColorBrush]::new($fillColor)
        }

        $pen = $null
        $stroke = $path.GetAttribute("stroke")
        if ($stroke -and $stroke -ne "none") {
            $strokeColor = [System.Windows.Media.ColorConverter]::ConvertFromString($stroke)
            $strokeBrush = [System.Windows.Media.SolidColorBrush]::new($strokeColor)
            $strokeWidth = [double]$path.GetAttribute("stroke-width")
            $pen = [System.Windows.Media.Pen]::new($strokeBrush, $strokeWidth)
            if ($path.GetAttribute("stroke-linecap") -eq "round") {
                $pen.StartLineCap = [System.Windows.Media.PenLineCap]::Round
                $pen.EndLineCap = [System.Windows.Media.PenLineCap]::Round
            }
            $pen.LineJoin = [System.Windows.Media.PenLineJoin]::Round
        }

        $drawing.DrawGeometry($brush, $pen, $geometry)
    }

    $drawing.Pop()
    $drawing.Close()

    $bitmap = [System.Windows.Media.Imaging.RenderTargetBitmap]::new(
        $PixelWidth,
        $PixelHeight,
        96,
        96,
        [System.Windows.Media.PixelFormats]::Pbgra32
    )
    $bitmap.Render($visual)

    $encoder = [System.Windows.Media.Imaging.PngBitmapEncoder]::new()
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($bitmap))
    $stream = [System.IO.File]::Create($Target)
    try {
        $encoder.Save($stream)
    } finally {
        $stream.Dispose()
    }
}

$artwork = Join-Path $ProjectRoot "artwork"
$drawable = Join-Path $ProjectRoot "watchface\src\main\res\drawable"

Convert-SvgToPng (Join-Path $artwork "hour_passenger_plane.svg") (Join-Path $drawable "hour_passenger_plane.png") 192 816
Convert-SvgToPng (Join-Path $artwork "minute_fighter_jet.svg") (Join-Path $drawable "minute_fighter_jet.png") 160 640
Convert-SvgToPng (Join-Path $artwork "debug_hour_center_dot.svg") (Join-Path $drawable "debug_hour_center_dot.png") 24 752
Convert-SvgToPng (Join-Path $artwork "debug_minute_center_dot.svg") (Join-Path $drawable "debug_minute_center_dot.png") 24 568
Convert-SvgToPng (Join-Path $artwork "radar_sweep.svg") (Join-Path $drawable "radar_sweep.png") 8 406
Convert-SvgToPng (Join-Path $artwork "radar_sweep_glow.svg") (Join-Path $drawable "radar_sweep_glow.png") 28 406

Write-Output "Rendered WFF hand assets from the SVG masters."
