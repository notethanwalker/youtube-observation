# Desktop-only setup and launch. No tunnel or public network binding is configured.
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))

function Refresh-CommandPath {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
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
            $result = & $exe @prefix -c 'import sys; print("OK" if sys.version_info >= (3, 12) else "OLD")' 2>$null
            if ($LASTEXITCODE -eq 0 -and $result -eq 'OK') { return $candidate }
        } catch { continue }
    }
    return $null
}

$python = Find-UsablePython
$hasMediaTools = (Get-Command ffmpeg -ErrorAction SilentlyContinue) -and
                 (Get-Command ffprobe -ErrorAction SilentlyContinue)
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
    $hasMediaTools = (Get-Command ffmpeg -ErrorAction SilentlyContinue) -and
                     (Get-Command ffprobe -ErrorAction SilentlyContinue)
    if (-not $python -or -not $hasMediaTools) {
        throw 'Installation completed but the commands are not on PATH yet. Close this window, open the launcher again, and retry.'
    }
}

foreach ($secret in @('OPENAI_API_KEY', 'MATCH_REVIEW_PASSWORD')) {
    if (-not [Environment]::GetEnvironmentVariable($secret, 'Process')) {
        $secure = Read-Host "Enter $secret (hidden; kept in this session only)" -AsSecureString
        $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
        try {
            $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
            if ([string]::IsNullOrWhiteSpace($plain)) { throw "$secret cannot be empty." }
            Set-Item -Path ("Env:" + $secret) -Value $plain
        } finally {
            [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
            Remove-Variable plain -ErrorAction SilentlyContinue
        }
    }
}

Write-Host 'Capitology review: http://127.0.0.1:8080'
Write-Host 'Username: player. Keep this window open while a review runs.'
$exe = $python.Command
$prefix = $python.Prefix
& $exe @prefix -m match_review.server --host 127.0.0.1 --port 8080
