param(
    [Parameter(Mandatory=$true)]
    [string]$Url,

    [ValidateSet("motion","standard")]
    [string]$Preset = "motion",

    [ValidateSet(360,480,720,1080)]
    [int]$MaxHeight = 1080,

    [string]$CookiesFile = "$env:USERPROFILE\Downloads\youtube_cookies.txt",

    [ValidateSet("firefox","edge","chrome")]
    [string]$Browser = "firefox"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing required command: $Name"
    }
}

Require-Command "yt-dlp"
Require-Command "python"
Require-Command "ffmpeg"
Require-Command "ffprobe"

$cookiePath = $null
$deleteCookieAfter = $false

if (Test-Path $CookiesFile) {
    $cookiePath = (Resolve-Path $CookiesFile).Path
    Write-Host "Using existing cookie file: $cookiePath"
} else {
    $cookiePath = Join-Path $env:TEMP ("youtube-observation-cookies-" + [guid]::NewGuid().ToString() + ".txt")
    $deleteCookieAfter = $true
    Write-Host "No cookie file found at $CookiesFile"
    Write-Host "Exporting authenticated cookies from $Browser..."
    & yt-dlp --cookies-from-browser $Browser --cookies $cookiePath --simulate $Url
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $cookiePath)) {
        throw "Could not export browser cookies."
    }
}

$outDir = Join-Path $repoRoot "observation_output"
if (Test-Path $outDir) {
    Remove-Item $outDir -Recurse -Force
}

try {
    Write-Host "Running observation ingest locally through your residential connection..."
    $argsList = @(
        "$PSScriptRoot\ingest.py",
        $Url,
        "--preset", $Preset,
        "--max-height", $MaxHeight,
        "--output", $outDir,
        "--cookies-file", $cookiePath
    )
    & python @argsList

    if ($LASTEXITCODE -ne 0) {
        throw "Observation ingest failed with exit code $LASTEXITCODE."
    }

    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $zipPath = Join-Path $repoRoot "youtube-observation-$stamp.zip"
    if (Test-Path $zipPath) {
        Remove-Item $zipPath -Force
    }

    Compress-Archive -Path (Join-Path $outDir "*") -DestinationPath $zipPath -CompressionLevel Fastest

    Write-Host ""
    Write-Host "Observation pack complete:"
    Write-Host $zipPath
    Write-Host ""
    Write-Host "Upload this ZIP to ChatGPT for analysis."
}
finally {
    if ($deleteCookieAfter -and $cookiePath -and (Test-Path $cookiePath)) {
        Remove-Item $cookiePath -Force
    }
}
