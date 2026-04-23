# Troubleshooting

Common problems and how to fix them. Written for Roula's Claude Code agent to scan when she describes a problem — paste the symptom into the search box here, the agent executes the fix.

---

## Setup

### `python: command not found`

The user's Python isn't on PATH, or Python isn't installed.

**Fix (Windows):**
```powershell
# Try the Python launcher instead
py --version
# If that works, use py everywhere instead of python:
py run.py setup
# If NOT installed:
winget install -e --id Python.Python.3.11
# Restart the terminal.
```

### `Python 3.x.x is too old. Need Python 3.11+`

`run.py` detected an older Python. Install 3.11+ via winget and re-run.

### `.env.txt exists!` during `setup_check`

Windows hides the `.txt` extension by default, and Notepad saved `.env` as `.env.txt`.

**Fix:** delete the `.env.txt` file and re-run `python run.py setup`. `run.py` will copy `.env.example` → `.env` correctly. **Never ask the user to edit `.env` in Notepad by hand.**

### `pip install` fails with permission error

Don't run as admin. Make sure you're installing into the venv, not the system Python. `run.py` handles this — use `python run.py setup`, not a bare `pip install`.

### `run.py setup` runs forever / appears to hang

First-run installs can take 60–90 seconds (streamlit + yfinance + plotly are large). If it exceeds 3 minutes, kill the terminal and re-run — pip may be stuck on a mirror.

---

## Running the dashboard

### `Dashboard already running (PID X)` but browser shows nothing

The `.streamlit.pid` file is stale — the process is gone but the file wasn't cleaned up.

**Fix:**
```powershell
python run.py stop
python run.py start
```

### `Port 8501 already in use`

Another app (or a leftover Streamlit process) is on the port.

**Fix on Windows:**
```powershell
# Find what's using it
netstat -ano | findstr :8501
# Kill it by PID
taskkill /PID <pid> /F
# Restart
python run.py start
```

### Dashboard opens but the page is blank

Usually a Python error during view render.

**Fix:**
```powershell
python run.py stop
# Run streamlit in the foreground so errors surface:
.\.venv\Scripts\python.exe -m streamlit run app.py
# Read the red stack trace, fix the view file, restart:
python run.py start
```

### Every ticker shows `—` for price / metrics

yfinance is temporarily unavailable. Not a bug. Click **Refresh** in the sidebar. If still empty after 5 min, Yahoo Finance may be throttling — try again in an hour.

The Overview tab will show an explicit error banner when all tickers fail. If you see that banner, no action is needed other than waiting or checking network connectivity.

---

## API keys

### Added my Finnhub key but the sidebar still shows ⚪ `finnhub`

Streamlit cached the "no key" state. Restart:
```powershell
python run.py stop && python run.py start
```

### `setup_check.py` reports the key as detected, but news/earnings panels say "add your Finnhub key"

Same as above — restart. Streamlit reads `.env` at app boot.

### Invalid Finnhub key rejected

Possible causes, in order of likelihood:
1. Key not activated yet (fresh signups take ~5 min — wait and retry)
2. Copy-paste picked up whitespace — open `.env`, remove spaces around the `=`
3. Wrong value pasted — check <https://finnhub.io/dashboard>
4. Free tier exhausted (60 calls/min — unlikely for personal use)

### Alpha Vantage returning no data

Free tier is 25 calls/**day**, 5/minute. If you've been using it heavily, it's rate-limited for the day. The orchestrator automatically falls back to yfinance so the dashboard keeps working.

---

## AI Briefing

### Briefing button is disabled with "Monthly Anthropic budget reached"

You've hit `ANTHROPIC_MONTHLY_BUDGET_USD` (default $5.00). By design, the only way to re-enable before month-end is to manually raise that value in `.env`.

**Fix:**
```
# In .env, edit:
ANTHROPIC_MONTHLY_BUDGET_USD=10.00
```
Then restart the dashboard. The meter shows the new cap immediately.

### Button shows "Wait N minutes" — how do I override?

Rate limit: default 1 briefing per hour. Set by `ANTHROPIC_MIN_MINUTES_BETWEEN_BRIEFINGS` in `.env`. To lower it:
```
ANTHROPIC_MIN_MINUTES_BETWEEN_BRIEFINGS=15
```
Restart the dashboard.

### Got a 429 error when generating

Anthropic rate-limited the request. Per PRD §5.6 #8, the app does not retry automatically. Wait a few minutes and try again.

### Briefing generated but the cache file has weird YAML at the top

That's intentional — YAML frontmatter with provenance (timestamp, model, tokens, cost). If you open `briefings/2026-04-21.md` in a plain text editor, you'll see it. When you download via the dashboard button, it's included for your records. The dashboard itself strips it before rendering.

### I want to clear my usage ledger

The ledger is at `briefings/.usage.jsonl`. Deleting the file resets your monthly spend to $0 — but **this is self-defeating**: the cap exists to stop you from going over by accident. Raising the cap in `.env` is almost always the right move instead.

If you really want to clear it (e.g. corrupt file):
```powershell
# Windows
del briefings\.usage.jsonl
```

---

## Adding / editing tickers

### Added a ticker to `tickers.yaml`, dashboard still shows the old list

Streamlit caches `Settings` per process. Click the sidebar **Refresh** button, or restart the dashboard.

### Ticker symbol not recognized by yfinance

Some foreign tickers need a suffix: `TSLA` (US) works, but `SHOP.TO` (Shopify on TSX), `VOD.L` (Vodafone on LSE), `005930.KS` (Samsung on KOSPI) need exchange suffixes. yfinance uses Yahoo's symbol conventions.

### How do I reset to the original 5-ticker list?

```powershell
git checkout config/tickers.yaml
# If not a git repo or no changes checked in yet, manually restore to:
# CRDO, HIMS, BABA, QQQI, IREN (see config/tickers.yaml in the upstream repo)
```

---

## Windows specifics

### The `🔄 Refresh data` button does nothing

Very rare. Usually the click registers but the cache wasn't cleared. Stop and restart:
```powershell
python run.py stop && python run.py start
```

### `Microsoft Defender SmartScreen` blocked a script

Allow the script through. The warning is for unsigned binaries, which `run.py` isn't — but Windows can occasionally flag `streamlit run` scripts during first launch.

### Terminal output shows garbled characters

`setup_check.py` and `run.py` force UTF-8 stdout explicitly, but if you're running a non-project script in an older cmd.exe, set:
```powershell
chcp 65001
```
before running to switch the codepage to UTF-8.

---

## When none of the above helps

1. Run `python run.py setup` — it validates the environment and reports what's off.
2. Check the Streamlit log — run in foreground: `.\.venv\Scripts\python.exe -m streamlit run app.py`
3. Post the exact error message (no screenshots) to your agent. Include the last 10 lines of the stack trace.

The agent should:
- Read the traceback top-to-bottom
- Identify the file + line number
- Fix the root cause, not the symptom
- Re-run tests: `python run.py test`
