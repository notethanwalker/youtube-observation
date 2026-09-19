param(
    [string]$RepoUrl = "https://github.com/notethanwalker/youtube-observation.git",
    [string]$InstallDir = "$env:USERPROFILE\youtube-observation"
)

$ErrorActionPreference = "Stop"

function Ensure-WingetPackage {
    param([string]$Id, [string]$Command)
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        Write-Host "$Command already installed."
        return
    }
    Write-Host "Installing $Id..."
    winget install --id $Id -e --accept-source-agreements --accept-package-agreements
}

Ensure-WingetPackage "Git.Git" "git"
Ensure-WingetPackage "Python.Python.3.12" "python"
Ensure-WingetPackage "Rclone.Rclone" "rclone"
Ensure-WingetPackage "yt-dlp.yt-dlp" "yt-dlp"

$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Host ""
    Write-Host "Git was installed but is not yet visible in this PowerShell session."
    Write-Host "Close PowerShell, reopen it, and run this bootstrap script again."
    exit 0
}

if (Test-Path (Join-Path $InstallDir ".git")) {
    Write-Host "Repository already exists; pulling latest changes."
    Push-Location $InstallDir
    git pull
    Pop-Location
} elseif (-not (Test-Path $InstallDir)) {
    git clone $RepoUrl $InstallDir
} else {
    throw "Install directory exists but is not a Git repository: $InstallDir"
}

Write-Host ""
Write-Host "Base tooling and repository are ready."
Write-Host "Next one-time steps require browser/account authorization:"
Write-Host "1. Run: rclone config"
Write-Host "   Create remote 'youtube-drive' using root folder ID 1ss2HxIPQbwJ2zPVuw5s1XTulPHc6sRLD"
Write-Host "2. Add the resulting rclone.conf as GitHub secret RCLONE_CONFIG_B64."
Write-Host "3. Register this PC under GitHub Settings -> Actions -> Runners as a Windows x64 self-hosted runner."
Write-Host "4. Keep the runner installed as a Windows service."
Write-Host ""
Write-Host "Full instructions:"
Write-Host (Join-Path $InstallDir "SETUP_HYBRID.md")
