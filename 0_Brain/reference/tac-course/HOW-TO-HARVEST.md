# Course transcript pipeline — how to capture the remaining lessons

Built 2026-08-03. Works on any Mux-hosted paywalled video where subtitles exist.
~3–6 min per lesson. Nothing leaves the machine; uses Kam's logged-in Chrome.

## Why this shape

The video is DRM-protected (`drm-token` on the `mux-player`), so downloading the
media is impossible — but Mux serves a **separate English subtitle track**. The
captions ARE the transcript, so no audio or transcription is needed.

## Procedure

1. **Navigate** (full page load — the SPA's own nav does NOT swap the player;
   always verify `h1` matches the intended lesson before harvesting).
2. **Init** — `document.querySelector('mux-player')`, set `muted`, call
   `.play()` (the `<video>` element does not exist until playback starts; it
   lives in nested shadow DOM — walk `shadowRoot` recursively to find it).
   Enable the `en` subtitles track (`track.mode='showing'`).
3. **Harvest by seeking** — subtitle segments load progressively. Step
   `video.currentTime` in 45 s increments, sleeping ~600 ms, collecting
   `track.cues` into a dict keyed by start time (dedupes automatically).
   **Keep each `javascript_tool` call under ~40 s of work** — the CDP bridge
   times out at 45 s. Long videos (~47 min) need 4–6 calls.
4. **Verify coverage** — check for gaps > 12 s between consecutive cues and that
   the last cue is near `video.duration`. Re-run ranges to fill holes.
5. **Extract** — render the transcript into the page
   (`document.body.innerHTML = '<pre id=wedout>'; textContent = text`) and call
   `get_page_text`. Output > ~50 KB is persisted to a file (best case — extract
   with Python, no context cost); under that it returns inline and is truncated
   at 50 000 characters, so **render in chunks below that** and stitch.

## Known blockers (all hit and diagnosed 2026-08-03)

- **Downloads**: `a.click()` downloads worked twice, then Chrome silently
  blocked further downloads from the origin (multiple-automatic-downloads
  policy). A real user-gesture click did NOT restore it. Don't rely on it.
- **Local receiver over HTTP**: blocked — mixed content (https page → http
  localhost). A receiver script exists at `2_Project_Files/tools/media/
  receiver.py` if an https path is ever available.
- **Clipboard API**: `navigator.clipboard.writeText` hangs (focus/permission).
- **`yt-dlp`**: cannot extract (site not supported, DRM anyway).

## Helpers on disk

- `2_Project_Files/tools/media/stitch.py` — merge transcript fragments by
  timestamp, dedupe, write to the transcripts folder.
- `2_Project_Files/tools/media/.venv` — yt-dlp + faster-whisper (unused for this
  course; kept for videos that lack captions and need real transcription).

## Status

| Lesson | Slug | Transcript on disk |
|---|---|---|
| 01 Hello Agentic Coding | `hello-agentic-coding` | ✅ verbatim |
| 02 The 12 Leverage Points | `the-12-leverage-points` | ✅ verbatim + reflowed |
| 03 Success is Planned | `success-is-planned` | ✅ verbatim |
| 04 AFK Agents | `afk-agents` | harvested + read; re-harvest to file |
| 05 Close The Loops | *(find via NEXT LESSON)* | ⬜ |
| 06 Agentic Review & Documentation | ⬜ | ⬜ |
| 07 ZTE: The Secret of Agentic Engineering | ⬜ | ⬜ |
| 08 The Agentic Layer | ⬜ | ⬜ |
| 09–14 Agentic Horizon (multi-agent, orchestrator, agent experts) | ⬜ | Kam's priority after 1–8 |
