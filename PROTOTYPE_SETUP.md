# Capitology match review prototype

A single-owner, password-protected upload and report application. The user uploads an exported Overwatch screen recording (MP4/MOV/MKV/WebM), optionally names the player, and receives a timecoded report linked to the provisional Pass 9 Capitology rules. An in-client replay code is not a video upload and is not supported.

## Desktop-only setup (Windows)

The default Windows trial runs on your PC and uses the Gemini API free tier for analysis. No OpenAI key, paid account, local vision model, Render, phone app, tunnel, public URL, or port forwarding is required. The original recording and reports stay on your PC; sampled still frames are sent to Google. Google says content sent to unpaid Gemini services may be used to improve its products. Free API usage is rate limited, so a full match may need to be retried later or use shorter clips. The PC and launcher must remain on during analysis. Coaching quality has not yet been validated on real matches.

1. [Download the project ZIP](https://github.com/notethanwalker/youtube-observation/archive/refs/heads/main.zip), extract it, and double-click **`START_CAPITOLOGY.cmd`** inside the extracted `youtube-observation` folder.
2. The launcher checks for Python 3.12+ and FFmpeg. If missing, it uses Windows Package Manager (`winget`) to install them. If `winget` is unavailable, install [Python](https://www.python.org/downloads/windows/) and [FFmpeg](https://ffmpeg.org/download.html) manually.
3. Get a **free** Gemini API key from [Google AI Studio](https://aistudio.google.com/api-keys). Create or select a project on its **Free** tier; do not enable billing for this prototype. On the API Keys page use the key's **Copy** button to copy the full active key (not the project ID or key name). The launcher asks for `GEMINI_API_KEY` on each run and a private review password, then verifies the key with Google before opening the upload page. It keeps them in the running process and does not write a config file. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) on the same PC. When the browser asks for credentials, use `player` as the username and the password you chose.

Keep the launcher window open during an upload and analysis. The default upload limit is 2 GiB and the maximum video duration is one hour. The browser remembers the last job on this PC while its data remains available. Running the launcher again resumes saved jobs and reports. Full-match tactical accuracy remains to be tested with your recordings.

If you already uploaded a match with an older ZIP: close the old launcher, extract the newest ZIP into a new folder, then copy the **entire** `match-review-data` folder from the old extracted project into the new project folder. Run the new `START_CAPITOLOGY.cmd`, enter a Gemini key and the same review password, revisit your existing localhost page, and click **Retry saved recording**. Do not upload or share the `match-review-data` folder; it contains your recording.

Local job files are in `match-review-data/`, excluded from Git. Delete a finished job from the report page when done. The same password grants access to all jobs in this single-owner prototype. Do not commit recordings, reports, or secrets to GitHub.

For a manual launch, open PowerShell in the extracted project folder and run `powershell -ExecutionPolicy Bypass -File .\scripts\start_match_review_windows.ps1`.

### Phone access later

When you want to use a phone, install [Tailscale](https://tailscale.com/docs/install) on the PC and phone and sign in to the same tailnet. With the local application running, `tailscale serve --bg http://127.0.0.1:8080` can create a private HTTPS URL for tailnet devices. [Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve) stays within the tailnet; do not use Funnel for this private trial. The desktop launcher does not configure Tailscale automatically.

## Run locally

Requirements: Python 3.12+, `ffmpeg`, `ffprobe`, and a free Gemini API key from Google AI Studio.

```bash
export MATCH_REVIEW_PROVIDER=gemini
export GEMINI_API_KEY='...'
export MATCH_REVIEW_PASSWORD='choose-a-long-private-password'
python -m match_review.server --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080` and sign in as `player` with the chosen password. The upload and report jobs are stored under `match-review-data/`, which is excluded from Git. The default upload cap is 2 GiB; the Render Blueprint sets 500 MiB because its free disk is temporary. Set `MATCH_REVIEW_MAX_UPLOAD_BYTES` to change it. Jobs between 15 seconds and one hour are accepted; a recording under five minutes is labeled a short recording review.

For a network binding, set `MATCH_REVIEW_PASSWORD` first and put the service behind HTTPS. The same password grants access to all jobs in this single-owner prototype. It is not a multi-user account system. A completed job can be deleted from its report page; deletion removes its source video, report, and corrections. Otherwise data remains on the configured volume until removed by an operator or lost with an ephemeral deployment. The report JSON can be downloaded. Do not store personal recordings in the Git repository or GitHub Actions artifacts.

## Processing and result

The server streams the original file to private job storage, checks its video stream and duration with FFprobe, and queues one analysis at a time. The broad pass samples a still every ten seconds over the recording, choosing at most two windows per two-minute section. The dense pass inspects up to eight windows with stills 2.5 seconds apart. In the default Gemini configuration, these sampled frames are sent to Google; the original video stays on your PC. Derived stills are deleted after analysis. Rule sources link to the channel research, not the uploaded match.

A finding requires identifiable player evidence, a visible action, a time range inside the sampled window, and a linked rule. It separates observations, interpretation, alternative, exception, confidence, and uncertainty. High confidence is capped at moderate because the service does not inspect intervening motion or audio. It may return an insufficient-evidence report. The feedback form stores corrections with the job; it does not automatically regenerate the report. The application does not infer exact ability order or hidden game state from the missing frames.

The Windows launcher defaults to `MATCH_REVIEW_PROVIDER=gemini`, model `gemini-3.5-flash-lite`. It supports image input and structured output on Google's free tier. The earlier `gemini-3.8-flash` default has a small free daily request allowance in some projects; a full review can need up to 38 requests. The older `gemini-2.5-flash` default is unavailable for some new projects. If your project has no Lite quota, inspect [its model-specific limits](https://aistudio.google.com/rate-limit); a new key in the same project does not reset them. Google's daily limits reset at midnight Pacific time. When switching from an older ZIP, copy the entire `match-review-data` folder as described above. A saved review retains completed sections when changing between Gemini models, and its JSON report records the models used. Lite's coaching quality still needs testing on real footage. An optional offline route uses `MATCH_REVIEW_PROVIDER=ollama` and the free local `qwen3-vl:4b-instruct` model (about 3.3 GB download; potentially slow on CPU). The optional paid route uses `MATCH_REVIEW_PROVIDER=openai` with an OpenAI API key. Model calls are sequential. The player can leave the page and resume from its URL while the app stays open.

## Internal check

```bash
python -m unittest discover -s tests -v
```

This uses a generated 16-second video and fake model endpoints to verify authentication, upload, FFmpeg sampling, model request shape, job/report delivery, video range requests, corrections, and deletion. It does **not** prove the model's coaching judgments are accurate. The 80-second project clip was also probed and sampled with FFmpeg. A real Gemini call and two full unedited match reviews with a knowledgeable player are still required to assess tactical quality and timestamp attribution.

## If a review stops with HTTP 429

A 429 can mean temporary API request/token limits **or** a Platform credit or spend limit. The updated application reads the API error code: it retries temporary throttling with short backoff, but stops promptly for billing or quota errors. After fixing the reported limit, choose **Retry saved recording** on the error page; you do not need to upload it again. Check your [API billing](https://platform.openai.com/settings/organization/billing/overview) and [limits](https://platform.openai.com/settings/organization/limits) if the message mentions credits or a spend limit. ChatGPT subscription billing does not fund API requests.

For an old ZIP, use the migration instructions above. The default Gemini path does not need OpenAI billing; it uses your Gemini free tier quota.

If Google reports `API_KEY_INVALID`, close the launcher, check that AI Studio shows the key as active and allowed for Gemini, then use its **Copy** button and rerun the launcher. The revised launcher discards any older Gemini key inherited from Windows, trims stray spaces or quotes, and checks the new key before another upload. Keep the saved `match-review-data` folder and retry the recording after the key is accepted. If a freshly created key still fails the check, try a new key in the same project and inspect AI Studio's key status; Google may block non-working or exposed keys. Do not send your key to anyone.

If Google reports HTTP 503 `UNAVAILABLE` or high demand, the Gemini model is temporarily overloaded. The updated app retries transient server errors with short backoff. If demand persists, use **Retry saved recording** later; completed analysis sections are checkpointed. Existing recordings do not need another upload.

If Google reports a free-tier limit, check [AI Studio's rate limits](https://aistudio.google.com/rate-limit) for the selected model and project. A daily limit needs the next reset; a temporary request limit may recover sooner. The app preserves completed sections so **Retry saved recording** continues the same job. A new API key under the same project does not add quota.

## Optional Render preview

`render.yaml` defines a free Docker web service, HTTPS URL, health check, 500 MiB upload cap, and two secrets supplied in the Render dashboard: `MATCH_REVIEW_PASSWORD` and `OPENAI_API_KEY`. Connect this GitHub repository to a Render Blueprint in the intended workspace. The service is reachable at its assigned `onrender.com` URL, with Basic Auth over HTTPS.

Render's free web service has an **ephemeral filesystem**. A redeploy or restart can erase uploads and reports; resume is possible only while the instance data persists. Treat this as a limited private trial. A durable later version needs persistent object storage or a paid service with a disk; neither is silently provisioned here. Free service resources and provider API calls may impose additional limits or charges. Avoid submitting sensitive personal footage to a trial that has not been reviewed for production use.

## Remaining acceptance work

1. Run a real free-tier Gemini call with the player's key to confirm quota, image handling, and structured output.
2. Start the desktop service on `127.0.0.1`; verify authentication, upload, completed report, playback, and correction in the local browser. Phone access and Render are optional.
3. Have the player upload two different full unedited matches, inspect the footage alongside every major finding, and correct false attribution or unsupported advice before calling the coaching quality validated.
