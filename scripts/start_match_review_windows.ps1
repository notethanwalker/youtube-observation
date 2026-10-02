# Desktop-only setup and launch. No tunnel or public network binding is configured.
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))
if (-not $env:MATCH_REVIEW_PROVIDER) { $env:MATCH_REVIEW_PROVIDER = 'gemini' }
if (-not $env:MATCH_REVIEW_LOCAL_MODEL) { $env:MATCH_REVIEW_LOCAL_MODEL = 'qwen3-vl:4b-instruct' }

function Refresh-CommandPath {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
}

function Find-MediaTools {
    if ((Get-Command ffmpeg -ErrorAction SilentlyContinue) -and
        (Get-Command ffprobe -ErrorAction SilentlyContinue)) { return $true }
    $locations = @(
        (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages'),
        (Join-Path $env:ProgramData 'chocolatey\lib\ffmpeg\tools')
    )
    foreach ($location in $locations) {
        if (-not (Test-Path $location)) { continue }
        $ffmpegExe = Get-ChildItem -Path $location -Filter ffmpeg.exe -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($ffmpegExe -and (Test-Path (Join-Path $ffmpegExe.DirectoryName 'ffprobe.exe'))) {
            $env:Path = $ffmpegExe.DirectoryName + ';' + $env:Path
            return $true
        }
    }
    return $false
}

function Find-UsablePython {
    $candidates = @(
        @{ Command = 'py'; Prefix = @('-3.12') },
        @{ Command = 'python'; Prefix = @() },
        @{ Command = 'py'; Prefix = @('-3') }
    )
    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) { continue }
        try {
            $exe = $candidate.Command
            $prefix = $candidate.Prefix
            & $exe @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>$null
            if ($LASTEXITCODE -eq 0) { return $candidate }
        } catch { continue }
    }
    return $null
}

$python = Find-UsablePython
$hasMediaTools = Find-MediaTools
if (-not $python -or -not $hasMediaTools) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw 'Python 3.12+ or FFmpeg is missing, and winget is unavailable. Install Python and FFmpeg using the links in PROTOTYPE_SETUP.md, then rerun.'
    }
    if (-not $python) {
        Write-Host 'Installing Python 3.12 with Windows Package Manager...'
        winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { throw 'Python installation did not finish. See the winget output above.' }
    }
    if (-not $hasMediaTools) {
        Write-Host 'Installing FFmpeg with Windows Package Manager...'
        winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { throw 'FFmpeg installation did not finish. See the winget output above.' }
    }
    Refresh-CommandPath
    $python = Find-UsablePython
    $hasMediaTools = Find-MediaTools
    if (-not $python -or -not $hasMediaTools) {
        throw "Installation finished, but tool lookup still failed (Python: $([bool]$python), FFmpeg/FFprobe: $hasMediaTools). Reopen the launcher and retry."
    }
}

if ($env:MATCH_REVIEW_PROVIDER -eq 'ollama') {
    $ollama = Get-Command ollama -ErrorAction SilentlyContinue
    $ollamaPath = Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama.exe'
    if (-not $ollama -and -not (Test-Path $ollamaPath)) {
        if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
            throw 'Ollama is missing. Install it from https://ollama.com/download/windows, then rerun the launcher.'
        }
        Write-Host 'Installing Ollama for free local vision analysis...'
        winget install --id Ollama.Ollama --exact --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0) { throw 'Ollama installation did not finish. See the winget output above.' }
        Refresh-CommandPath
        $ollama = Get-Command ollama -ErrorAction SilentlyContinue
    }
    if ($ollama) { $ollamaExe = $ollama.Source }
    elseif (Test-Path $ollamaPath) { $ollamaExe = $ollamaPath }
    else { throw 'Ollama was installed but not found. Reopen the launcher and retry.' }

    $ready = $false
    try { $null = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2; $ready = $true } catch {}
    if (-not $ready) {
        Write-Host 'Starting the local Ollama service...'
        Start-Process -FilePath $ollamaExe -ArgumentList 'serve' -WindowStyle Hidden
        for ($i = 0; $i -lt 30; $i++) {
            Start-Sleep -Seconds 1
            try { $null = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2; $ready = $true; break } catch {}
        }
    }
    if (-not $ready) { throw 'Ollama did not start on localhost:11434. Start the Ollama app and rerun the launcher.' }
    $models = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 10
    if (-not @($models.models | Where-Object { $_.name -eq $env:MATCH_REVIEW_LOCAL_MODEL }).Count) {
        Write-Host "Downloading local vision model $env:MATCH_REVIEW_LOCAL_MODEL (about 3.3 GB for the default; once only)..."
        & $ollamaExe pull $env:MATCH_REVIEW_LOCAL_MODEL
        if ($LASTEXITCODE -ne 0) { throw 'Vision model download did not finish. Rerun the launcher to resume.' }
    }
    Write-Host "Free local analysis ready: $env:MATCH_REVIEW_LOCAL_MODEL"
} elseif ($env:MATCH_REVIEW_PROVIDER -ne 'openai' -and $env:MATCH_REVIEW_PROVIDER -ne 'gemini') {
    throw 'MATCH_REVIEW_PROVIDER must be gemini, ollama, or openai.'
}

$secrets = @('MATCH_REVIEW_PASSWORD')
if ($env:MATCH_REVIEW_PROVIDER -eq 'openai') { $secrets += 'OPENAI_API_KEY' }
if ($env:MATCH_REVIEW_PROVIDER -eq 'gemini') {
    $secrets += 'GEMINI_API_KEY'
    # Ask each desktop session, even if Windows inherited an older key.
    if ($env:MATCH_REVIEW_SKIP_KEY_PREFLIGHT -ne '1') { Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue }
}
foreach ($secret in $secrets) {
    if (-not [Environment]::GetEnvironmentVariable($secret, 'Process')) {
        $secure = Read-Host "Enter $secret (hidden; kept in this session only)" -AsSecureString
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        try {
            $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
            if ([string]::IsNullOrWhiteSpace($plain)) { throw "$secret cannot be empty." }
            Set-Item -Path ("Env:" + $secret) -Value $plain.Trim()
        } finally {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
            Remove-Variable plain -ErrorAction SilentlyContinue
        }
    }
}

if ($env:MATCH_REVIEW_PROVIDER -eq 'gemini' -and $env:MATCH_REVIEW_SKIP_KEY_PREFLIGHT -ne '1') {
    # A metadata request checks the key before the user uploads a recording.
    $env:GEMINI_API_KEY = $env:GEMINI_API_KEY.Trim().Trim([char]34).Trim([char]39)
    Write-Host 'Checking the Gemini key with Google...'
    try {
        $null = Invoke-RestMethod -Uri 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash' -Headers @{ 'x-goog-api-key' = $env:GEMINI_API_KEY } -TimeoutSec 20
    } catch {
        $status = 0
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
        if ($status -eq 400 -or $status -eq 401) {
            throw 'Google did not accept this Gemini key. Copy the full active API key in AI Studio (not the project ID or key name), close this window, and rerun the launcher. Do not share the key.'
        }
        throw "Could not verify Gemini access (HTTP $status). Check the AI Studio key/project and your connection, then rerun the launcher."
    }
    Write-Host 'Gemini key accepted.'
}

Write-Host 'Capitology review: http://127.0.0.1:8080'
Write-Host 'Username: player. Keep this window open while a review runs.'
$exe = $python.Command
$prefix = $python.Prefix
& $exe @prefix -m match_review.server --host 127.0.0.1 --port 8080
