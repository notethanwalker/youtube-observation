# Capitology match review prototype

A single-owner, password-protected upload and report application. The user uploads an exported Overwatch screen recording (MP4/MOV/MKV/WebM), optionally names the player, and receives a timecoded report linked to the provisional Pass 9 Capitology rules. An in-client replay code is not a video upload and is not supported.

## Recommended: run on your own PC and phone

This avoids Render. The PC holds the recordings and runs FFmpeg and the analysis service; [Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve) gives your phone a private HTTPS URL reachable only when both devices are signed in to the same tailnet. The PC must stay on with the application running for uploads and jobs to finish. No port forwarding, public site, or rented server is needed. Tailscale's Personal plan is currently free for personal use; model API usage remains separately billed. Avoid `tailscale funnel`, which opens a public URL.

On Windows, install [Python 3.12+](https://www.python.org/downloads/windows/), [FFmpeg](https://ffmpeg.org/download.html) so `ffmpeg` and `ffprobe` are on PATH, and [Tailscale](https://tailscale.com/download) on both the PC and phone. Sign in to the same tailnet. Download or clone this repository, open PowerShell in its root, and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_match_review_windows.ps1
```

The launcher prompts for the model API key and private review password without writing either to a file, configures private Tailscale Serve, displays the tailnet URL, and starts the server on loopback. Open the HTTPS URL shown by `tailscale serve status` on your phone with Tailscale connected. Sign in as `player` with the review password and upload a recording. Keep the PowerShell window open. The URL is available only inside the tailnet. If Tailscale is absent, the page works locally at `http://127.0.0.1:8080` until it is installed.

Recordings and reports stay under `match-review-data/` on the PC (excluded from Git). The player can delete a finished job in the page. Sampled still frames are sent to the model API for analysis, so this avoids Render storage but does not avoid the external model provider. Back up or delete local recordings as desired. The service is single-user; the password guards all its jobs.

## Run locally

Requirements: Python 3.12+, `ffmpeg`, `ffprobe`, and an OpenAI API key with access to the configured image-capable Responses model.

```bash
export OPENAI_API_KEY='...'
export MATCH_REVIEW_PASSWORD='choose-a-long-private-password'
python -m match_review.server --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080` and sign in as `player` with the chosen password. The upload and report jobs are stored under `match-review-data/`, which is excluded from Git. The default upload cap is 2 GiB; the Render Blueprint sets 500 MiB because its free disk is temporary. Set `MATCH_REVIEW_MAX_UPLOAD_BYTES` to change it. Jobs between 15 seconds and one hour are accepted; a recording under five minutes is labeled a short recording review.

For a network binding, set `MATCH_REVIEW_PASSWORD` first and put the service behind HTTPS. The same password grants access to all jobs in this single-owner prototype. It is not a multi-user account system. A completed job can be deleted from its report page; deletion removes its source video, report, and corrections. Otherwise data remains on the configured volume until removed by an operator or lost with an ephemeral deployment. The report JSON can be downloaded. Do not store personal recordings in the Git repository or GitHub Actions artifacts.

## Processing and result

The server streams the original file to private job storage, checks its video stream and duration with FFprobe, and queues one analysis at a time. The broad pass samples a still every ten seconds over the recording, choosing at most two windows per two-minute section. The dense pass inspects up to eight windows with stills 2.5 seconds apart. Only these stills are sent to the model provider; the uploaded file stays on the application host. Derived stills are deleted after analysis. Rule sources link to the channel research, not the uploaded match.

A finding requires identifiable player evidence, a visible action, a time range inside the sampled window, and a linked rule. It separates observations, interpretation, alternative, exception, confidence, and uncertainty. High confidence is capped at moderate because the service does not inspect intervening motion or audio. It may return an insufficient-evidence report. The feedback form stores corrections with the job; it does not automatically regenerate the report. The application does not infer exact ability order or hidden game state from the missing frames.

The two model names can be set with `MATCH_REVIEW_BROAD_MODEL` and `MATCH_REVIEW_DENSE_MODEL` (defaults: `gpt-5-mini`). `OPENAI_BASE_URL` defaults to the OpenAI API base URL. The application uses the Responses API with base64 image inputs and a strict JSON schema. Model calls are sequential and may take several minutes. The player can leave and resume the job from its URL on the same device while the data remains available.

## Internal check

```bash
python -m unittest discover -s tests -v
```

This uses a generated 16-second video and a local fake Responses endpoint to verify authentication, upload, FFmpeg sampling, model request shape, job/report delivery, video range requests, corrections, and deletion. It does **not** prove the model's coaching judgments are accurate. The 80-second project clip was also probed and sampled with FFmpeg. A live API call and two full unedited match reviews with a knowledgeable player are still required to assess tactical quality and timestamp attribution. User video testing begins after the local service and model credential are ready.

## Optional Render preview

`render.yaml` defines a free Docker web service, HTTPS URL, health check, 500 MiB upload cap, and two secrets supplied in the Render dashboard: `MATCH_REVIEW_PASSWORD` and `OPENAI_API_KEY`. Connect this GitHub repository to a Render Blueprint in the intended workspace. The service is reachable at its assigned `onrender.com` URL, with Basic Auth over HTTPS.

Render's free web service has an **ephemeral filesystem**. A redeploy or restart can erase uploads and reports; resume is possible only while the instance data persists. Treat this as a limited private trial. A durable later version needs persistent object storage or a paid service with a disk; neither is silently provisioned here. Free service resources and provider API calls may impose additional limits or charges. Avoid submitting sensitive personal footage to a trial that has not been reviewed for production use.

## Remaining acceptance work

1. Configure the model API key, perform one live call, and confirm the schema and image request on the chosen account.
2. Start the local PC service with Tailscale Serve; verify authentication, upload, completed report, playback, and correction on the private phone URL. Render is optional.
3. Have the player upload two different full unedited matches, inspect the footage alongside every major finding, and correct false attribution or unsupported advice before calling the coaching quality validated.
