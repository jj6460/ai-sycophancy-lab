param(
    [Parameter(Mandatory=$true)][string]$PdfPath,
    [Parameter(Mandatory=$true)][string]$OutDir,
    [string]$Lang = "en-US",
    [int]$Dpi = 300
)

$ErrorActionPreference = "Stop"
$py = "C:\Users\ljw\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"

# 1) render pages to PNG with PyMuPDF
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$renderScript = @'
import pymupdf, sys, os
pdf, outdir, dpi = sys.argv[1], sys.argv[2], int(sys.argv[3])
doc = pymupdf.open(pdf)
os.makedirs(outdir, exist_ok=True)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=dpi)
    pix.save(os.path.join(outdir, 'page_%03d.png' % (i+1)))
print('rendered', doc.page_count)
'@
$renderScript | Out-File -Encoding utf8 (Join-Path $OutDir "render.py")
& $py (Join-Path $OutDir "render.py") $PdfPath $OutDir $Dpi

# 2) OCR each page with Windows.Media.Ocr
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime]
Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
})[0]

function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}

$language = [Windows.Globalization.Language]::new($Lang)
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($language)
if ($null -eq $engine) { throw "Could not create OCR engine for $Lang" }

$files = Get-ChildItem -Path $OutDir -Filter "page_*.png" | Sort-Object Name
$sb = New-Object System.Text.StringBuilder
foreach ($f in $files) {
    $sf = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
    $stream = Await ($sf.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("========== PAGE $($f.BaseName) ==========")
    foreach ($line in $result.Lines) { [void]$sb.AppendLine($line.Text) }
    $stream.Dispose()
    Write-Host ("OCR done: " + $f.Name + " lines=" + $result.Lines.Count)
}

$outFile = Join-Path $OutDir "ocr_text.txt"
[System.IO.File]::WriteAllText($outFile, $sb.ToString(), [System.Text.Encoding]::UTF8)
Write-Host "WROTE $outFile"
