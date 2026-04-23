# Equity Research Desk

A local-first equity research dashboard — Python + Streamlit + Plotly, powered by yfinance (no API key required). Zero-key start, graceful upgrade when Finnhub / Alpha Vantage / Claude keys are added.

> **Audience note.** This README is written for an AI coding agent (Claude Code) to parse and execute. The user is **non-technical**, on **Windows 11**, and will say things like *"Clone this and set it up for me."* Clarity for the agent beats prose for a human reader.

---

## Tech stack

- Python 3.11+
- Streamlit ≥ 1.31 (uses `st.dialog` in Phase 4)
- yfinance — primary data source, no key
- Plotly — charts
- Optional: Finnhub (news + earnings), Alpha Vantage (backup fundamentals), Anthropic Claude Sonnet 4.6 (AI briefings, Phase 4)

---

## Bootstrap — for an agent setting this up on a fresh machine

The user is non-technical. Do not ask her to install anything manually. If a prerequisite is missing, install it yourself (with her one-time consent for each `winget` command). Work through these steps **in order**. Stop and ask her for help **only** if all automated paths fail.

### Step 1 — Verify / install Python 3.11+

```powershell
# Windows 11 — check first:
python --version      # or: py --version

# If missing, install via winget (Windows 11 has winget by default):
winget install -e --id Python.Python.3.11

# Then restart the terminal so PATH picks up the new python.
```

If `winget` itself is missing (rare on Windows 11): install from <https://www.python.org/downloads/> — pick 3.11 or 3.12, tick **"Add Python to PATH"** at the top of the installer.

### Step 2 — Verify / install Git

```powershell
git --version

# If missing:
winget install -e --id Git.Git
```

Fallback: <https://git-scm.com/download/win>.

### Step 3 — Clone the repo

```powershell
git clone https://github.com/seanmccloskey10-cell/equity-research-desk
cd equity-research-desk
```

### Step 4 — One-command setup

```powershell
python run.py setup
```

That's it. `run.py` handles:

- Creating a local `.venv` (isolated — does not touch the user's other Python projects)
- Installing `requirements.txt` into the venv
- Copying `.env.example` to `.env` if missing
- Running `setup_check.py` (validates Python, deps, `.env`, and does a yfinance live smoke test)

### Step 5 — Start the dashboard

```powershell
python run.py start
```

Open <http://localhost:8501> in her browser. Tell her the dashboard is running.

### Step 6 — Stop the dashboard (later)

```powershell
python run.py stop
```

---

## Daily commands the agent should recognize

Everything routes through `run.py` so the agent never has to remember venv paths.

| User says | Agent runs |
|---|---|
| "Start the dashboard" | `python run.py start` |
| "Stop the dashboard" | `python run.py stop` |
| "Refresh the data" | Click the sidebar refresh button; OR `python run.py stop && python run.py start` |
| "Check if setup is working" | `python run.py setup` |
| "Run the tests" | `python run.py test` |
| "Add TSLA to my watchlist" | Append to [config/tickers.yaml](config/tickers.yaml) under `tickers:`, then tell user to hit Refresh |
| "Remove X from my watchlist" | Remove from [config/tickers.yaml](config/tickers.yaml) |
| "Help me add my Finnhub key" | Open `.env`, set `FINNHUB_API_KEY=<value>`; `python run.py setup` to verify |

More prompts in [PROMPTS.md](PROMPTS.md).

---

## Windows traps (Roula is on Windows 11 — read this)

1. **Hidden `.txt` extension.** File Explorer hides known extensions. If she creates `.env` in Notepad, Windows may save it as `.env.txt`. `setup_check.py` detects this. Fix: have the agent copy `.env.example` → `.env` via the CLI (`copy .env.example .env`) so she never sees the trap.

2. **Forward slashes only in Python paths.** The code uses `pathlib.Path` everywhere; agents extending the code must do the same.

3. **PowerShell vs bash.** She may have either terminal open. All project commands route through `python run.py <cmd>`, which works identically in both.

4. **`pip` not on PATH.** Don't call `pip` directly. `run.py` uses `.venv/Scripts/python.exe -m pip`, which always works.

5. **`python` vs `py`.** If `python --version` fails but `py --version` works, use `py run.py ...`. This happens when Python was installed via the Microsoft Store; the `py` launcher is installed alongside standard Python installers.

---

## Where to learn the code

Agent: read [CLAUDE.md](CLAUDE.md) before modifying anything. Code map, extension patterns, and the non-negotiable rules (Settings tab is read-only, Anthropic calls only from `views/briefing.py`, etc.).

When something breaks, [TROUBLESHOOTING.md](TROUBLESHOOTING.md) is the scan-first reference.

Everyone: [PRD.md](PRD.md) is the full spec. [APIS.md](APIS.md) is the menu of additional data sources Roula can add.

---

## Current build status

- **Phase 0** — scaffold ✅
- **Phase 1** — yfinance MVP ✅ (Overview + Detail tabs live)
- **Phase 2** — visual polish ✅ (candlestick + volume, inline sparklines, custom CSS theme)
- **Phase 3** — Finnhub + Alpha Vantage + Comparison tab ✅ (news/earnings unlock with Finnhub key)
- **Phase 4** — AI Briefing with full §5.6 budget protection ✅ (confirmation dialog, rate limit, hard cap, usage ledger, same-day cache)
- **Phase 5** — docs completion + more prompts ✅ (TROUBLESHOOTING.md + expanded PROMPTS.md)
- **Phase 6** — fresh-clone smoke test + polish — pending
