# YouTube Observation

Zero-cost YouTube media ingestion for ChatGPT-assisted visual analysis.

## Purpose

This repository turns an accessible YouTube URL into an **analysis pack** using GitHub Actions, `yt-dlp`, and FFmpeg. It is designed so a YouTube link can be submitted without requiring a local download step.

The pack contains:

- source video (up to 1080p by default)
- 60-second motion-analysis clips
- timestamped contact sheets
- extracted audio
- available subtitles/captions
- metadata and a manifest

## Starting a run

### Owner-only issue trigger

Create an issue whose title starts with:

`OBSERVE`

Put the YouTube URL anywhere in the issue body. For example:

```text
Title: OBSERVE jiu-jitsu round

https://youtu.be/VIDEO_ID
preset: motion
```

Only issues opened by the repository owner are allowed to start the ingestion job. This prevents public users from consuming Actions resources.

Recognized optional settings in the issue body:

- `preset: motion` — 60-second clips and denser visual sampling; best for sports, jiu-jitsu, demonstrations, mechanics
- `preset: standard` — 120-second clips and lighter sampling
- `height: 720` or `height: 1080` — requested maximum source height

If no preset is specified, `motion` is used.

### Manual GitHub UI trigger

The workflow also supports **Actions → Observe YouTube → Run workflow** with URL, preset, and max-height inputs.

## Output

Each successful run creates a GitHub Actions artifact named roughly:

`youtube-observation-<run id>`

Artifacts are intentionally temporary and are retained for 7 days to avoid unnecessary storage use.

## ChatGPT workflow

1. Send ChatGPT a YouTube URL.
2. ChatGPT can create an owner-authorized `OBSERVE` issue using the connected GitHub account.
3. GitHub Actions retrieves and processes the media.
4. ChatGPT can inspect the workflow status and retrieve the artifact through the GitHub connector.
5. The actual media can then be analyzed rather than relying on metadata or captions alone.

## Notes

- Use this only for media you are authorized to download/process and in accordance with applicable platform terms and law.
- Some private, DRM-protected, members-only, deleted, age/account-restricted, or bot-protected videos may not be retrievable from a GitHub-hosted runner.
- YouTube changes its delivery behavior periodically, so `yt-dlp` is installed fresh on every run.
- GitHub-hosted runners have finite disk space. Very long/high-resolution videos may require a lower height or a more selective extraction mode in a future version.
