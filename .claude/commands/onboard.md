<!-- AGENT-FACING — written for Claude Code, not for the tool's owner. -->

# /onboard — Set up the Equity Research Desk (make it theirs, then run it)

Run this right after the owner has cloned this repo. It does two jobs: **disconnect their copy from the public template** so it's 100% theirs, then **get the dashboard running** on a starter watchlist of well-known stocks, and show them how to make it their own.

The owner is **non-technical** and AI-fluent. They will NOT type commands, edit code, or read stack traces — you do all of that. Plain language with them, no jargon (no "venv", "PID", "yfinance" unless you explain it). Show what you're about to do, never push through an error: if something breaks, stop and tell them in plain words exactly what's wrong.

**Triggers (natural language):** "set this up for me", "get my stock dashboard running", "my tutor gave me this to install", or the owner pasted a handoff prompt that routes here.

## Step 0 — Make this copy the owner's OWN (git safety — do this FIRST)

The owner cloned this from a **public** template. Disconnect it before anything else.

1. Run `git remote -v`. If `origin` points at an `equity-research-desk` (or any template) repo, the copy is still linked to it.
2. Tell the owner, plainly: *"Right now this folder is still linked to the public template I was copied from. I'm going to disconnect it so your copy is 100% yours and private — your watchlist and any keys you add later can never be sent back to that public place. Okay?"*
3. On yes: `git remote remove origin` (keeps their local history). If they'd rather a totally clean slate, `rm -rf .git` (PowerShell: `Remove-Item -Recurse -Force .git`) then `git init`. **Default to `git remote remove origin`.**
4. Confirm `.gitignore` already excludes `.env` (it does). Their keys and watchlist stay local-only unless they later choose a *private* backup. Never a public repo.

## Step 1 — Prerequisites check (don't assume)

Verify before installing. On **Windows use PowerShell, not Git Bash** (Git Bash resolves some commands to the wrong binary and gives confusing output).

- **Git:** `git --version`
- **Python 3.11+:** `python --version` — if that fails, try `py --version` (Windows Python Launcher). On macOS use `python3 --version`. **Use whichever launcher works for every later command, consistently.**
- **VS Code:** `where.exe code` on Windows / `which code` on macOS.
- **Plan auth, NOT an API key:** confirm there's no `ANTHROPIC_API_KEY` env var set (Windows: `Get-Item Env:\ANTHROPIC_API_KEY -ErrorAction SilentlyContinue`; macOS: `echo $ANTHROPIC_API_KEY` — should be empty). The dashboard does not need it.

If any are missing, **stop** and point them at `PREREQUISITES.md`. Don't try to install system software silently.

> macOS note: the first `git` command may trigger a "install command line developer tools" popup. That's normal — tell them to click **Install** and wait (~5 min), then continue.

## Step 2 — Set up (one command, you run it)

- Run `python run.py setup` (or `py run.py setup` / `python3 run.py setup` per Step 1). This creates the virtual environment, installs dependencies (~1 min first time), creates `.env` from `.env.example`, and runs a self-check.
- **Never ask the owner to create or edit `.env` by hand** — especially not in Notepad (Windows hides the `.txt` extension and silently makes `.env.txt`, which breaks it). If `.env` ever needs editing, you do it.
- Report each step in plain language. If the self-check fails, read its message and `TROUBLESHOOTING.md` before guessing.

## Step 3 — Start it and verify (the real "done" check)

- Run `python run.py start`. Then tell the owner to open **http://localhost:8501**.
- **Verify, don't assume:** the sidebar shows the watchlist with **NVDA showing a live price** (a real number, not a dash or an error), and there are no red error banners. Only then say it's working.
- If port 8501 is busy, the start script will tell you — follow its message (stop the old process or it'll point you to the fix) rather than reporting a false success.

## Step 4 — Show them it's theirs to grow

- Explain: *"This ships with a few well-known stocks so it looks alive — they're a starting point, not a limit. We can swap in the ones you actually follow."*
- Demo it: ask which stock they follow, then **you** add it to `config/tickers.yaml` (or replace the starter list with theirs) and hit Refresh so they watch it appear. (Adding a bad symbol just shows a dash — harmless.)
- Tell them how to ask next time: *"Add TSLA to my watchlist", "show me NVDA's P/E"* — see `PROMPTS.md`.

## Step 5 — Stop here

- **Do NOT** set up the optional Anthropic API key for AI Briefings. That's a deliberate later add-on (it's billed per-token, separate from their Claude plan, with a hard monthly cap). Mention it exists; don't install it now unless they explicitly ask.

## If you get stuck

Read `HELP.md` and `TROUBLESHOOTING.md` (Windows vs macOS gotchas, common errors) **before** guessing or asking the owner. If still stuck, tell them exactly what's wrong in plain language and stop — don't push through.

## Rules

- Step 0 (git detach) is mandatory. Do it before anything else.
- Show every command/edit before running it. Keep them in the loop at each major step.
- Never edit `.env` in a GUI editor; never ask the owner to.
- Never install system software (Python, Git) silently — point at `PREREQUISITES.md`.
- Verify the live NVDA price before claiming success. "It started" ≠ "it works".
