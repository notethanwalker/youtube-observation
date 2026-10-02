param(
  [string]$RequestPath = 'requests/capitology-pass6-batch.json',
  [string]$QueuePath = 'research/capitology-model/pass06_retrieval_queue.csv',
  [string]$OutputPath = 'pass06_output'
)

$ErrorActionPreference = 'Stop'
$request = Get-Content $RequestPath -Raw | ConvertFrom-Json
$ids = @($request.video_ids)
$rows = @(Import-Csv $QueuePath)
if ($ids.Count -lt 1 -or $ids.Count -gt 4 -or (@($ids | Select-Object -Unique)).Count -ne $ids.Count) {
  throw 'Expected one to four unique video IDs'
}
foreach ($id in $ids) {
  if ($id -notmatch '^[A-Za-z0-9_-]{11}$' -or -not @($rows | Where-Object video_id -eq $id).Count) {
    throw "Invalid or unqueued video ID: $id"
  }
}

New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
foreach ($sub in @('clips', 'frames')) {
  New-Item -ItemType Directory -Path (Join-Path $OutputPath $sub) -Force | Out-Null
}
$manifest = @{batch_key=$request.batch_key; video_ids=$ids; media='silent 480p-or-lower clips; original timecodes'; windows=@(); failures=@()}
$manifestPath = Join-Path $OutputPath 'manifest.json'
$manifest | ConvertTo-Json -Depth 8 | Set-Content $manifestPath -Encoding UTF8

$yt = Join-Path $env:RUNNER_TEMP 'capitology-pass6-yt-dlp.exe'
if (-not (Test-Path $yt)) {
  Invoke-WebRequest -Uri 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe' -OutFile $yt
}
$runnerRoot = Split-Path (Split-Path $env:RUNNER_TEMP -Parent) -Parent
$node = Join-Path $runnerRoot 'externals\node24\bin\node.exe'
if (-not (Test-Path $node)) { $node = Join-Path $runnerRoot 'externals\node20\bin\node.exe' }
if (-not (Test-Path $node)) { throw 'Node executable missing on runner' }
$jsArgs = @('--js-runtimes', ('node:' + $node), '--remote-components', 'ejs:github', '--no-cache-dir')

$toolDir = Join-Path $env:RUNNER_TOOL_CACHE 'capitology-pass6-ffmpeg'
$ffmpeg = Get-ChildItem $toolDir -Filter ffmpeg.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
if (-not $ffmpeg) {
  New-Item -ItemType Directory -Path $toolDir -Force | Out-Null
  $ffmpegZip = Join-Path $env:RUNNER_TEMP 'capitology-pass6-ffmpeg.zip'
  Invoke-WebRequest -Uri 'https://github.com/yt-dlp/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl-shared.zip' -OutFile $ffmpegZip
  Expand-Archive -LiteralPath $ffmpegZip -DestinationPath $toolDir -Force
  $ffmpeg = Get-ChildItem $toolDir -Filter ffmpeg.exe -Recurse | Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ffmpeg) { throw 'Portable FFmpeg executable missing' }

$cookiePath = $null
if ($env:YOUTUBE_COOKIES_B64) {
  $cookiePath = Join-Path $env:RUNNER_TEMP 'capitology-pass6-batch-cookies.txt'
  [System.IO.File]::WriteAllBytes($cookiePath, [Convert]::FromBase64String($env:YOUTUBE_COOKIES_B64))
}
try {
  foreach ($videoId in $ids) {
    $sourceDir = Join-Path $env:RUNNER_TEMP ('capitology-pass6-' + $videoId)
    New-Item -ItemType Directory -Path $sourceDir -Force | Out-Null
    try {
      $url = 'https://www.youtube.com/watch?v=' + $videoId
      $source = $null
      foreach ($mode in @('anonymous', 'cookies')) {
        if ($mode -eq 'cookies' -and -not $cookiePath) { continue }
        Get-ChildItem $sourceDir -Filter 'source.*' -File | Remove-Item -Force
        $authArgs = @()
        if ($mode -eq 'cookies') { $authArgs = @('--cookies', $cookiePath) }
        $template = Join-Path $sourceDir 'source.%(ext)s'
        Write-Host ("Downloading $videoId ($mode)")
        & $yt @jsArgs --no-playlist --no-progress --no-warnings --force-overwrites @authArgs -f 'bv*[height<=480]/b[height<=480]/best[height<=480]' -o $template $url
        if ($LASTEXITCODE -eq 0) {
          $source = Get-ChildItem $sourceDir -Filter 'source.*' -File | Where-Object Length -gt 10000 | Select-Object -First 1 -ExpandProperty FullName
        }
        if ($source) { break }
      }
      if (-not $source) { throw "No video source retrieved for $videoId" }
      foreach ($row in @($rows | Where-Object video_id -eq $videoId)) {
        try {
          $start = [int]$row.start_seconds
          $end = [int]$row.end_seconds
          $duration = $end - $start
          $base = "$($row.window_id)_${videoId}_${start}-${end}"
          $clipName = "$base.mp4"
          $clipPath = Join-Path (Join-Path $OutputPath 'clips') $clipName
          & $ffmpeg -hide_banner -loglevel error -y -ss $start -i $source -t $duration -an -c:v libx264 -crf 22 -preset veryfast $clipPath
          if ($LASTEXITCODE -ne 0 -or -not (Test-Path $clipPath) -or (Get-Item $clipPath).Length -lt 10000) {
            throw 'Clip encode failed'
          }
          $frames = @()
          foreach ($check in @(@{label='start';offset=0}, @{label='middle';offset=[int][math]::Floor($duration/2)}, @{label='end';offset=$duration-1})) {
            $frameName = "$base`_$($check.label).jpg"
            $framePath = Join-Path (Join-Path $OutputPath 'frames') $frameName
            & $ffmpeg -hide_banner -loglevel error -y -ss $check.offset -i $clipPath -frames:v 1 $framePath
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path $framePath) -or (Get-Item $framePath).Length -lt 1000) {
              throw "Missing $($check.label) check frame"
            }
            $frames += 'frames/' + $frameName
          }
          $manifest.windows += @{window_id=$row.window_id;video_id=$videoId;start_seconds=$start;end_seconds=$end;
            clip=('clips/' + $clipName);clip_size_bytes=(Get-Item $clipPath).Length;
            clip_sha256=(Get-FileHash $clipPath -Algorithm SHA256).Hash.ToLowerInvariant();
            check_frames=$frames;retrieval_status='retrieved_video_only';visual_review_status='not_reviewed'}
          Write-Host ("Captured $($row.window_id): $clipName")
        } catch {
          $manifest.failures += @{window_id=$row.window_id;error=$_.Exception.Message}
        }
      }
    } catch {
      $manifest.failures += @{video_id=$videoId;error=$_.Exception.Message}
    } finally {
      $manifest | ConvertTo-Json -Depth 8 | Set-Content $manifestPath -Encoding UTF8
      Get-ChildItem $sourceDir -Filter 'source.*' -File | Remove-Item -Force
    }
  }
} finally {
  if ($cookiePath -and (Test-Path $cookiePath)) { Remove-Item $cookiePath -Force }
}
Write-Host ("Captured $($manifest.windows.Count) windows; $($manifest.failures.Count) failures")
if ($manifest.failures.Count -gt 0) { throw 'One or more queued windows failed; see manifest' }
