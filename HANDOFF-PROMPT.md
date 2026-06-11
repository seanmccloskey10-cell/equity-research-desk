# HANDOFF-PROMPT.md — Paste this into your Claude agent

The fastest way to install this tool: open VS Code, start your Claude agent (the Claude Code CLI via `claude` in the terminal, **or** the Claude VS Code extension chat panel — both work), then paste **one** of the two prompts below. Pick the one matching your OS. The agent enters plan mode first, tells you what's already on your machine, asks for one "go," then handles the entire setup.

## ⚠ Read this first — install prerequisites before pasting the handoff prompt

The handoff prompts below assume you already have:

- **Git**
- **Python 3.11+**
- **VS Code**
- **A Claude agent** in VS Code — the Claude Code CLI (`claude` in a terminal) **or** the Claude VS Code extension chat panel. Either works for this install.
- **Authenticated to a Claude plan** (not via an `ANTHROPIC_API_KEY` env var)

**If any of those are missing, run [PREREQUISITES.md](PREREQUISITES.md) FIRST.** The prerequisites prompt batches every install into one elevated session (one Apple GUI password dialog on Mac, one UAC popup on Windows) so you don't drown in permission prompts.

The handoff prompts below check prerequisites at the top. If they're missing, the agent will tell you to go run PREREQUISITES.md first.

The prompts are **deliberately verbose**. They bake in six lessons from prior user research:

1. **Plan mode FIRST** — the agent must report what it found before doing anything
2. **Permissions ack'd up front** — no surprise dialogs mid-execution
3. **GUI password dialogs / native UAC, NEVER terminal sudo** — same security, different trust feel
4. **Read README + CLAUDE.md before running anything** — the codebase has invariants that matter
5. **"What done looks like"** — the agent verifies concrete checks before claiming success
6. **Don't fix what isn't broken without approval** — known gaps stay unless you say otherwise

---

## Mac variant — paste this if you're on macOS

```
Someone built me a small equity (stock) research dashboard they want
me to install on my Mac. I follow the markets and I'm AI-fluent (heavy
Claude user), but I'm not a developer — I won't type commands, edit
code, or debug stack traces. You handle setup, config, and any
code-level adjustments via natural-language requests from me.

I want you to clone and set up this tool for me:

    https://github.com/seanmccloskey10-cell/equity-research-desk

It's a local-first stock dashboard — Python + Streamlit + Plotly,
powered by yfinance for live prices. It runs entirely on my Mac,
nothing leaves the machine except the optional AI Briefing call (which
uses an Anthropic API key — separate from any Claude plan, billed
per-token, with a hard monthly cap). It works fully WITHOUT that key.

OS HANDOFF — IMPORTANT
This tool's README leans macOS-first, which suits me, but it was
originally built and dry-run tested on Windows. If you spot any
Windows-specific assumptions in the code or docs, catch them as you go
and adjust silently — don't ask me what to do about a `.streamlit.pid`
file or whether to use `python` vs `python3`. The `run.py` wrapper is
cross-platform; just use `python3` on my machine consistently.

PREREQUISITES CHECK — DO THIS FIRST
Before anything else, verify I have the prerequisites installed:
- Git: `git --version`
- Python 3.11+: `python3 --version`
- VS Code: `which code`
- Plan auth (NOT API key): you should be using my Claude plan login —
  NOT an `ANTHROPIC_API_KEY` env var. Check `echo $ANTHROPIC_API_KEY`
  (should be empty or unset).

If ANY of those are missing or wrong, STOP and tell me. I'll go run
the prerequisites prompt at PREREQUISITES.md in this same repo
(https://github.com/seanmccloskey10-cell/equity-research-desk/blob/main/PREREQUISITES.md)
to install them properly in one batch — then come back here.

If all prerequisites are good, proceed.

I'll say "go" once when you ask. Don't ask again per command.

Please follow this flow:

1. ENTER PLAN MODE FIRST. After confirming prerequisites, tell me
   which README steps you'll follow and anything in the repo that
   looks like it needs a macOS adjustment. Don't start running
   anything until I say "go".

2. Read README.md and CLAUDE.md end-to-end before running anything.
   The README has the full bootstrap walkthrough; CLAUDE.md has the
   non-negotiable rules and explains how the codebase is organized
   (Settings tab is read-only, Anthropic API calls only from
   views/briefing.py, etc.).

3. Read PRD.md if you need full product context. It's a generic
   equity research dashboard spec — not personalized to any specific
   user.

4. Clone the repo into ~/Projects/equity-research-desk (create the
   Projects folder if it doesn't exist). On the first git command macOS
   may pop up "install command line developer tools" — that's normal,
   click Install and wait, then carry on.

4b. DISCONNECT my copy from the public template so it's mine and
   private: run `git remote remove origin` inside the folder. My
   watchlist and any keys I add later should never be able to go back
   to the public repo.

5. Open the cloned folder in VS Code.

6. Run `python3 run.py setup`. This creates a .venv, installs deps,
   copies .env.example to .env, and runs setup_check.py. Report each
   step.

7. Run `python3 run.py start` to start the dashboard. Then open
   http://localhost:8501 in my browser.

8. Stop when the dashboard is running and the watchlist shows a live
   price. DO NOT volunteer to set up the optional Anthropic API key
   for AI Briefings — that's a deliberate add-on for later.

WHAT "DONE" LOOKS LIKE — tell me ONLY when you've verified ALL of these:
- The folder ~/Projects/equity-research-desk/ exists with README.md,
  CLAUDE.md, PRD.md, run.py, app.py, .venv/, config/tickers.yaml.
- `python3 --version` shows 3.11 or newer.
- `python3 run.py setup` ran to completion with no errors.
- `python3 run.py start` is running; the dashboard is reachable at
  http://localhost:8501.
- The dashboard sidebar shows the watchlist — this template ships
  with a starter watchlist (NVDA, AAPL, MSFT, GOOGL, TSLA).
- NVDA shows a live price (not a dash, not an error).
- No red error banners on screen.

If any of those aren't right, don't say "it's working" — stop and
tell me exactly what's off.

A FEW THINGS ABOUT THIS REPO YOU SHOULD KNOW
This is a GENERIC TEMPLATE. The watchlist is intentionally seeded with
a few well-known stocks (NVDA, AAPL, MSFT, GOOGL, TSLA). The architecture supports as many
tickers as I want — I'll add my own later by asking you, or you can
edit config/tickers.yaml. The starter list is just a starting point — swap in your own anytime.

If you spot example tickers like CRDO or AAPL inside the test files
(tests/), leave them — that's internal test data, not something I see,
and the tests assert on it. Don't "tidy" it.

If settings ever need changing, edit the .env file YOURSELF — never ask
me to open it in Notepad or TextEdit. On Windows those hide the .txt
extension and silently save it as .env.txt, which breaks setup.

If you hit anything unexpected during setup — network failure, a
dependency install error, or anything that asks me to type my password
into a terminal — STOP and ask me before continuing. Don't silently
skip or work around anything.

Report back at each major step. Keep me in the loop.

Let's begin — please run the prerequisites check and tell me what you
find.
```

---

## Windows variant — paste this if you're on Windows

```
Someone built me a small equity (stock) research dashboard they want
me to install on my Windows PC. I follow the markets and I'm AI-fluent
(heavy Claude user), but I'm not a developer — I won't type commands,
edit code, or debug stack traces. You handle setup, config, and any
code-level adjustments via natural-language requests from me.

I want you to clone and set up this tool for me:

    https://github.com/seanmccloskey10-cell/equity-research-desk

It's a local-first stock dashboard — Python + Streamlit + Plotly,
powered by yfinance for live prices. It runs entirely on my PC,
nothing leaves the machine except the optional AI Briefing call (which
uses an Anthropic API key — separate from any Claude plan, billed
per-token, with a hard monthly cap). It works fully WITHOUT that key.

OS HANDOFF — IMPORTANT
This tool's README leans Mac-first in its narrative and code examples.
I'm on Windows 11. The repo has a "Windows notes" section and the
`run.py` wrapper is cross-platform, but catch Mac-isms as you go and
adjust silently — don't ask me what to do about `.streamlit.pid` or
whether to use `python3` vs `python`. Use `python` (or `py` if the
Python Launcher is what's installed) on my machine consistently.

PREREQUISITES CHECK — DO THIS FIRST
Before anything else, verify I have the prerequisites installed.
USE POWERSHELL for the version checks (NOT bash / git-bash — bash on
Windows resolves some commands differently and gives confusing
output). Specifically:
- Git: `git --version`
- Python 3.11+: `python --version` (and `py --version` as fallback)
- VS Code: `where.exe code` (NOT bare `code --version` — on Windows in
  bash, `code` may resolve to a Node.js binary inside VS Code's
  bundled folder and return a Node version like v22.x. Use
  `where.exe code` to see candidates, or run `code.cmd --version`.)
- Plan auth (NOT API key): you should be using my Claude plan login —
  NOT an `ANTHROPIC_API_KEY` env var. Check
  `Get-Item Env:\ANTHROPIC_API_KEY -ErrorAction SilentlyContinue`
  (should return empty).

If ANY of those are missing or wrong, STOP and tell me. I'll go run
the prerequisites prompt at PREREQUISITES.md in this same repo
(https://github.com/seanmccloskey10-cell/equity-research-desk/blob/main/PREREQUISITES.md)
to install them properly in one batched session — then come back here.

If all prerequisites are good, proceed.

I'll say "go" once when you ask. Don't ask again per command.

Please follow this flow:

1. ENTER PLAN MODE FIRST. After confirming prerequisites, tell me
   which README steps you'll follow and anything in the repo that
   looks like it needs a Windows adjustment. Don't start running
   anything until I say "go".

2. Read README.md and CLAUDE.md end-to-end before running anything.
   The README has the full bootstrap walkthrough; CLAUDE.md has the
   non-negotiable rules and explains how the codebase is organized
   (Settings tab is read-only, Anthropic API calls only from
   views/briefing.py, etc.).

3. Read PRD.md if you need full product context. It's a generic
   equity research dashboard spec — not personalized to any specific
   user.

4. Clone the repo into %USERPROFILE%\Projects\equity-research-desk
   (create the Projects folder if it doesn't exist).

4b. DISCONNECT my copy from the public template so it's mine and
   private: run `git remote remove origin` inside the folder. My
   watchlist and any keys I add later should never be able to go back
   to the public repo.

5. Open the cloned folder in VS Code.

6. Run `python run.py setup`. This creates a .venv, installs deps,
   copies .env.example to .env, and runs setup_check.py. Report each
   step. (If `python` doesn't work, try `py run.py setup` — the
   Windows Python Launcher.)

7. Run `python run.py start` to start the dashboard. Then open
   http://localhost:8501 in my browser.

8. Stop when the dashboard is running and the watchlist shows a live
   price. DO NOT volunteer to set up the optional Anthropic API key
   for AI Briefings — that's a deliberate add-on for later.

WHAT "DONE" LOOKS LIKE — tell me ONLY when you've verified ALL of these:
- The folder C:\Users\<me>\Projects\equity-research-desk\ exists with
  README.md, CLAUDE.md, PRD.md, run.py, app.py, .venv\,
  config\tickers.yaml.
- `python --version` (or `py --version`) shows 3.11 or newer.
- `python run.py setup` ran to completion with no errors.
- `python run.py start` is running; the dashboard is reachable at
  http://localhost:8501.
- The dashboard sidebar shows the watchlist — this template ships
  with a starter watchlist (NVDA, AAPL, MSFT, GOOGL, TSLA).
- NVDA shows a live price (not a dash, not an error).
- No red error banners on screen.

If any of those aren't right, don't say "it's working" — stop and
tell me exactly what's off.

A FEW THINGS ABOUT THIS REPO YOU SHOULD KNOW
This is a GENERIC TEMPLATE. The watchlist is intentionally seeded with
a few well-known stocks (NVDA, AAPL, MSFT, GOOGL, TSLA). The architecture supports as many
tickers as I want — I'll add my own later by asking you, or you can
edit config\tickers.yaml. The starter list is just a starting point — swap in your own anytime.

If you spot example tickers like CRDO or AAPL inside the test files
(tests\), leave them — that's internal test data, not something I see,
and the tests assert on it. Don't "tidy" it.

If settings ever need changing, edit the .env file YOURSELF — never ask
me to open it in Notepad or TextEdit. On Windows those hide the .txt
extension and silently save it as .env.txt, which breaks setup.

If you hit anything unexpected during setup — network failure, a
dependency install error, or anything that asks me to type my password
into a terminal — STOP and ask me before continuing. Don't silently
skip or work around anything.

Report back at each major step. Keep me in the loop.

Let's begin — please run the prerequisites check (in PowerShell, not
bash) and tell me what you find.
```

---

## After setup — what to say next

Once the dashboard is running, you drive it in plain language. Examples (full list in [PROMPTS.md](PROMPTS.md)):

- *"Add AAPL and MSFT to my watchlist."*
- *"Show me NVDA's P/E and profit margin."*
- *"Set up the AI Briefing — here's my Anthropic key: …"* (optional, costs pennies, hard monthly cap)
