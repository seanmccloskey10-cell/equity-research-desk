<!-- AGENT-FACING — written for Claude Code, not for the tool's owner. -->

# /setup — Re-run setup / repair the dashboard

Use this when the desk is already cloned and the owner wants to (re)install, restart, or fix it — e.g. "it won't start", "set it up again", "I closed it, bring it back". For a brand-new clone straight from the public template, use `/onboard` instead (it adds the git-detach step).

The owner is **non-technical** — you run all commands. Plain language, show before doing, never push through an error.

## Flow

1. **Launcher:** use whichever Python works — `python`, or `py` (Windows Launcher), or `python3` (macOS). Pick one and stay consistent. On Windows, **PowerShell, not Git Bash**.
2. **Setup:** `python run.py setup` — (re)creates the virtual environment, installs/updates dependencies, ensures `.env` exists, runs the self-check. Report each step. Never hand-edit `.env` (Notepad makes `.env.txt` on Windows — you edit it if needed).
3. **Start:** `python run.py start` → open **http://localhost:8501**. If it says the dashboard is already running, that's fine. If port 8501 is busy, follow the script's message (stop the stale process) instead of reporting success.
4. **Verify:** the watchlist shows **NVDA with a live price**, no red banners. Only then say it's working.
5. **Stop the dashboard** when asked: `python run.py stop`.

## Common fixes

- **`python` not found (Windows):** try `py run.py setup`. If neither works, Python isn't on PATH — point them at `PREREQUISITES.md`.
- **Port already in use:** the start script reports it. Stop the old process (the script/`TROUBLESHOOTING.md` gives the exact command), then start again.
- **Self-check fails on `.env.txt`:** delete the stray `.env.txt` and re-run setup; `.env` must have no extension. You create it, never the owner in Notepad.
- **Anything else:** read `HELP.md` / `TROUBLESHOOTING.md` before guessing.

## Rules
- Don't set up the optional Anthropic AI-Briefing key unless the owner explicitly asks (billed per-token, hard monthly cap, separate from their Claude plan).
- Show every command before running it; stop and explain on any error.
