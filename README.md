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

The user (Roula) is non-technical and on **macOS**. Do not ask her to install anything manually. If a prerequisite is missing, install it yourself (with her one-time consent per install command). Work through these steps **in order**. Stop and ask her for help **only** if all automated paths fail.

> **If you're running this on Windows** (e.g. Sean testing from his dev machine), swap `python3` for `python` (or `py`), and use `winget` in place of `brew`. Specific Windows equivalents are listed in the "Windows notes" section below.

### Step 1 — Verify / install Python 3.11+

macOS ships with an older Apple-supplied Python; you need 3.11 or newer.

```bash
# Check first — macOS should have python3 as a command:
python3 --version

# If missing, or version is < 3.11, prefer Homebrew:
brew --version       # check if Homebrew is installed

# If Homebrew is installed:
brew install python@3.11

# If Homebrew is NOT installed, install it first:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Then: brew install python@3.11

# Fallback (no Homebrew, GUI installer): download from https://www.python.org/downloads/
# Pick 3.11 or 3.12, run the .pkg installer. It adds `python3` to PATH automatically.
```

After install, restart the Terminal so PATH picks up the new `python3`.

### Step 2 — Verify / install Git

macOS doesn't ship Git by default but triggers an install prompt the first time you run `git`.

```bash
git --version
# If Git is missing, macOS pops up a dialog: "The git command requires the command line developer tools."
# Click Install. Takes ~5 minutes.

# Alternatively, if Homebrew is available:
brew install git
```

### Step 3 — Clone the repo

```bash
# Clone into her Projects folder (create if missing)
mkdir -p ~/Projects && cd ~/Projects
git clone https://github.com/seanmccloskey10-cell/equity-research-desk
cd equity-research-desk
```

### Step 4 — One-command setup

```bash
python3 run.py setup
```

That's it. `run.py` handles:

- Creating a local `.venv` (isolated — does not touch the user's other Python projects)
- Installing `requirements.txt` into the venv
- Copying `.env.example` to `.env` if missing
- Running `setup_check.py` (validates Python, deps, `.env`, and does a yfinance live smoke test)

### Step 5 — Start the dashboard

```bash
python3 run.py start
```

Open <http://localhost:8501> in her browser (macOS: `open http://localhost:8501` opens the default browser). Tell her the dashboard is running.

### Step 6 — Stop the dashboard (later)

```bash
python3 run.py stop
```

---

## Daily commands the agent should recognize

Everything routes through `run.py` so the agent never has to remember venv paths.

| User says | Agent runs (macOS) | Agent runs (Windows) |
|---|---|---|
| "Start the dashboard" | `python3 run.py start` | `python run.py start` |
| "Stop the dashboard" | `python3 run.py stop` | `python run.py stop` |
| "Refresh the data" | Click the sidebar refresh button; OR stop + start | (same) |
| "Check if setup is working" | `python3 run.py setup` | `python run.py setup` |
| "Run the tests" | `python3 run.py test` | `python run.py test` |
| "Add TSLA to my watchlist" | Append to [config/tickers.yaml](config/tickers.yaml) under `tickers:`, then tell user to hit Refresh | (same) |
| "Remove X from my watchlist" | Remove from [config/tickers.yaml](config/tickers.yaml) | (same) |
| "Help me add my Finnhub key" | Edit `.env`, set `FINNHUB_API_KEY=<value>`, then restart dashboard | (same) |

More prompts in [PROMPTS.md](PROMPTS.md).

---

## macOS notes — read before first setup

1. **Use `python3`, not `python`.** On macOS, `python` either doesn't exist or points to an old Apple-supplied Python 2/3.9. All commands in this repo use `python3` on macOS.

2. **TextEdit's rich-text default.** If the agent needs to edit `.env` by hand, don't open it in TextEdit — by default TextEdit saves `.rtf`, not plain text. Use VS Code (`code .env`) or `nano .env` in Terminal instead. Better: the agent should edit `.env` directly via its file-editing tools, never hand-off to Roula.

3. **Finder extension-hiding.** macOS Finder hides file extensions by default for recognised types. A file that looks like `.env` in Finder might actually be `.env.rtf` on disk. Verify in Terminal with `ls -la` — it shows the real name.

4. **Homebrew is the default package manager.** Most open-source Mac tools assume Homebrew is installed. If Roula doesn't have it, install it (step 1) — it's a one-time setup that makes every future install trivial.

5. **`.DS_Store` files.** macOS Finder sprinkles these everywhere. `.gitignore` already excludes them — nothing to worry about.

6. **First-run Gatekeeper prompt.** Python scripts don't trigger Gatekeeper (the unsigned-binary blocker), so this isn't a concern here. Relevant only if installing downloaded apps.

---

## Windows notes (for Sean testing, or future Windows students)

If you're running this on Windows instead of macOS:

1. **Command swap.** Use `python` (or `py`) instead of `python3`. The `run.py` wrapper handles cross-platform venv paths internally; only the launching command differs.

2. **Python install.** `winget install -e --id Python.Python.3.11` (Windows 11 has `winget` by default). Fallback: <https://www.python.org/downloads/> — tick **"Add Python to PATH"** at the top of the installer.

3. **Git install.** `winget install -e --id Git.Git`. Fallback: <https://git-scm.com/download/win>.

4. **Hidden `.txt` extension.** File Explorer hides known extensions. If `.env` is ever opened in Notepad, Windows may save it as `.env.txt`. `setup_check.py` detects this trap. Fix: agent uses `copy .env.example .env` via the CLI so the file is never Notepad-mangled.

5. **`pip` not on PATH.** Don't call `pip` directly. `run.py` uses `.venv/Scripts/python.exe -m pip`, which always works.

6. **`python` vs `py`.** If `python --version` fails but `py --version` works, use `py run.py ...` — happens when Python was installed via the Microsoft Store; the `py` launcher ships with standard Python installers.

7. **PowerShell vs cmd vs bash.** All project commands route through `python run.py <cmd>`, which works identically in any terminal.

---

## Where to learn the code

Agent: read [CLAUDE.md](CLAUDE.md) before modifying anything. Code map, extension patterns, and the non-negotiable rules (Settings tab is read-only, Anthropic calls only from `views/briefing.py`, etc.).

**When something breaks**: [HELP.md](HELP.md) is the first stop — it has a single prompt you paste to your agent that runs a full diagnostic across Python, `.env`, keys, dashboard, and connectivity. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) is the deeper reference for specific failure recipes.

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
