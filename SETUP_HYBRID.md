# Hybrid YouTube Observation Setup

This is the persistent, low-disk architecture for YouTube Observation.

## Architecture

1. A request is written to `requests/current.json` or the hybrid workflow is manually dispatched.
2. A Windows self-hosted GitHub Actions runner on the user's PC receives the job.
3. `yt-dlp` uses the user's residential IP and Firefox/YouTube cookies.
4. The selected YouTube stream is piped directly into `rclone rcat`.
5. The video is stored persistently in Google Drive without first being written to local disk.
6. A GitHub-hosted Ubuntu job downloads that stored source from Drive, creates motion-analysis clips/contact sheets/audio, and uploads the observation artifact for ChatGPT retrieval.

The user's PC only needs enough free disk space for the repository, tools, and normal program caches. The source video itself is streamed.

## Persistent storage

Google Drive folder:

- Name: `YouTube Observation Archive`
- Folder ID: `1ss2HxIPQbwJ2zPVuw5s1XTulPHc6sRLD`

The local rclone remote should be named exactly:

`youtube-drive`

and its root folder should be the folder ID above.

## One-time Windows setup

### 1. Install tools

Open PowerShell and run:

```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id Rclone.Rclone -e
winget install --id yt-dlp.yt-dlp -e
```

Close and reopen PowerShell after installation.

Verify:

```powershell
git --version
python --version
rclone version
yt-dlp --version
```

### 2. Clone the repository

```powershell
cd $env:USERPROFILE
git clone https://github.com/notethanwalker/youtube-observation.git
cd youtube-observation
```

### 3. Configure rclone for Google Drive

Run:

```powershell
rclone config
```

Create a new remote:

- name: `youtube-drive`
- storage: Google Drive
- scope: full Drive access
- root folder ID: `1ss2HxIPQbwJ2zPVuw5s1XTulPHc6sRLD`
- authenticate in the browser when prompted

Test:

```powershell
rclone lsf youtube-drive:
```

### 4. Put the same rclone configuration in the GitHub repository secret

Find the rclone config path:

```powershell
rclone config file
```

The usual location is:

`$env:APPDATA\rclone\rclone.conf`

Copy the Base64-encoded config to the clipboard:

```powershell
$configPath = "$env:APPDATA\rclone\rclone.conf"
$bytes = [System.IO.File]::ReadAllBytes($configPath)
[Convert]::ToBase64String($bytes) | Set-Clipboard
```

In GitHub:

`youtube-observation -> Settings -> Secrets and variables -> Actions -> New repository secret`

Create:

`RCLONE_CONFIG_B64`

and paste the clipboard contents.

Do not commit `rclone.conf` to the repository.

### 5. Configure Firefox authentication

Firefox is the preferred browser for YouTube cookie access on Windows.

Log into YouTube in Firefox once. The hybrid capture script will use the existing exported file at:

`$env:USERPROFILE\Downloads\youtube_cookies.txt`

when present. If that file is absent, it falls back to:

`--cookies-from-browser firefox`

Keep the Firefox YouTube session signed in. If YouTube invalidates the session later, log in again.

### 6. Register the PC as a GitHub self-hosted runner

Open:

`youtube-observation -> Settings -> Actions -> Runners -> New self-hosted runner`

Choose:

- Windows
- x64

Follow GitHub's commands to download and configure the runner in a small directory such as:

`C:\actions-runner`

When prompted whether to run as a service, choose **Yes**. This allows future requests to run without opening PowerShell manually.

The hybrid workflow expects the default labels:

- `self-hosted`
- `Windows`
- `X64`

No custom label is required.

## Future usage

After the one-time setup, the intended ChatGPT workflow is:

1. User sends a YouTube link in chat.
2. ChatGPT writes that URL to `requests/current.json`.
3. The self-hosted Windows runner automatically streams the video directly to Google Drive.
4. The cloud processing job creates the observation pack.
5. ChatGPT retrieves the finished artifact and analyzes the actual footage.

No manual download, local video storage, or repeated cookie/GitHub setup should be required.

## Manual test

Once setup is complete, update `requests/current.json` or run:

`Actions -> Observe YouTube Hybrid -> Run workflow`

Use:

`https://www.youtube.com/watch?v=Qn9JO2Ozh5Q`

with preset `motion`.

## Storage behavior

The master source video remains in Google Drive until the user deletes it. GitHub analysis artifacts are temporary and retained for 7 days. This avoids using GitHub as long-term media storage while preserving the original video for later re-analysis.
