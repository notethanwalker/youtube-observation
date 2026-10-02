# Start the single-owner match review on this PC only.
$ErrorActionPreference = 'Stop'
Set-Location (Resolve-Path (Join-Path $PSScriptRoot '..'))

foreach ($command in @('python', 'ffmpeg', 'ffprobe')) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "$command is missing. Install it and reopen PowerShell."
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

Write-Host 'Starting Capitology review at http://127.0.0.1:8080. Keep this PowerShell window open.'
python -m match_review.server --host 127.0.0.1 --port 8080
