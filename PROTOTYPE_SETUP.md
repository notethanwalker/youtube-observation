# Capitology match review prototype

A single-owner, password-protected upload and report application. The user uploads an exported Overwatch screen recording (MP4/MOV/MKV/WebM), optionally names the player, and receives a timecoded report linked to the provisional Pass 9 Capitology rules. An in-client replay code is not a video upload and is not supported.

## Desktop-only setup (Windows)

The first trial can run entirely on your PC. No Render, phone app, tunnel, public URL, or port forwarding is required. Recordings and reports stay on the PC; sampled still frames are sent to the model API. The PC must stay on and the launcher window must remain open during an upload and analysis. Model API usage is separately billed.

1. Install [Python 3.12+](https://www.python.org/downloads/windows/) and [FFmpeg](https://ffmpeg.org/download.html). Confirm `python`, `ffmpeg`, and `ffprobe` are on PATH by opening a new PowerShell window and running `python --version`, `ffmpeg -version`, and `ffprobe -version`.
2. Download the repository using GitHub's **Code → Download ZIP** and extract it, or clone it. In the extracted `youtube-observation` folder, open PowerShell.
3. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_match_review_windows.ps1
```

The launcher prompts for your OpenAI API key and a private review password, keeping both in that PowerShell session rather than writing a config file. It checks dependencies and starts the service bound to `127.0.0.1`. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) on the same PC. When the browser asks for credentials, use `player` as the username and the password you chose. Upload an exported MP4/MOV/MKV/WebM match recording. The browser remembers the last job on this PC while its data remains available. Closing the PowerShell window stops the service; running the script again resumes saved jobs and reports.

A ChatGPT subscription does not itself configure this app's API access; the launcher needs a separate OpenAI API key. No credential is included in GitHub. The default upload limit is 2 GiB and the maximum video duration is one hour. Full-match tactical accuracy remains to be tested with your recordings.

Local job files are in `match-review-data/`, excluded from Git. Delete a finished job from the report page when done. The same password grants access to all jobs in this single-owner prototype. Do not commit recordings, reports, or secrets to GitHub.

### Phone access later

When you want to use a phone, install [Tailscale](https://tailscale.com/docs/install) on the PC and phone and sign in to the same tailnet. With the local application running, `tailscale serve --bg http://127.0.0.1:8080` can create a private HTTPS URL for tailnet devices. [Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve) stays within the tailnet; do not use Funnel for this private trial. The desktop launcher does not configure Tailscale automatically.

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

This uses a generated 16-second video and a local fake Responses endpoint to verify authentication, upload, FFmpeg sampling, model request shape, job/report delivery, video range requests, corrections, and deletion. It does **not** prove the model's coaching judgments are accurate. The 80-second project clip was also probed and sampled with FFmpeg. A live API call and two full unedited match reviews with a knowledgeable player are still required to assess tactical quality and timestamp attribution. Player video testing begins after the desktop service and model credential are ready.

## Optional Render preview

`render.yaml` defines a free Docker web service, HTTPS URL, health check, 500 MiB upload cap, and two secrets supplied in the Render dashboard: `MATCH_REVIEW_PASSWORD` and `OPENAI_API_KEY`. Connect this GitHub repository to a Render Blueprint in the intended workspace. The service is reachable at its assigned `onrender.com` URL, with Basic Auth over HTTPS.

Render's free web service has an **ephemeral filesystem**. A redeploy or restart can erase uploads and reports; resume is possible only while the instance data persists. Treat this as a limited private trial. A durable later version needs persistent object storage or a paid service with a disk; neither is silently provisioned here. Free service resources and provider API calls may impose additional limits or charges. Avoid submitting sensitive personal footage to a trial that has not been reviewed for production use.

## Remaining acceptance work

1. Configure the model API key, perform one live call, and confirm the schema and image request on the chosen account.
2. Start the desktop service on `127.0.0.1`; verify authentication, upload, completed report, playback, and correction in the local browser. Phone access and Render are optional.
3. Have the player upload two different full unedited matches, inspect the footage alongside every major finding, and correct false attribution or unsupported advice before calling the coaching quality validated.
