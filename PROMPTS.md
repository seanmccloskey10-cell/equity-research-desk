# Prompts — what to say to your agent

Copy any line below, paste it to your Claude Code agent in VS Code, and hit Enter. Your agent reads this file and knows the patterns.

---

## Getting started

- *"Clone this repo and get it running for me: https://github.com/seanmccloskey10-cell/equity-research-desk"*
  — Your agent follows README's **Bootstrap** section: checks for Python 3.11+ and Git (installs via winget if missing), clones the repo, runs `python run.py setup`, then `python run.py start`. Dashboard opens at http://localhost:8501.
- *"I want to use this equity research tool — can you set it up?"*
- *"Check if the setup is working and let me know what I need to do next."*
  — Your agent runs `python run.py setup` and reports back.

## Using the dashboard

- *"Start the dashboard."*
- *"Stop the dashboard."*
- *"Refresh the data."*
- *"Open the dashboard in my browser."*
- *"Is the dashboard still running?"*

## Managing the watchlist

- *"Add TSLA to my watchlist."*
- *"Remove BABA from my watchlist."*
- *"What stocks am I tracking right now?"*
- *"Replace QQQI with VOO in my watchlist."*
- *"Reset my watchlist to the original five tickers."*

## Adding API keys

- *"Help me add my Finnhub API key to the project."*
- *"Help me add my Alpha Vantage API key to the project."*
- *"Help me add my Claude API key so I can get AI briefings."*
- *"Check which API keys I currently have set up."*

## AI Briefing

- *"Generate an AI briefing for me."*
  — Opens the briefing tab; you click the button yourself (the confirmation dialog is on purpose, to prevent surprise costs).
- *"Download today's briefing as a markdown file."*
  — Use the ⬇ Download .md button inside the briefing panel.
- *"Show me my briefing history."*
  — List files in `briefings/` directory.
- *"Delete the briefing from <date>."*
- *"What's in the briefing prompt template?"*
  — Agent reads `config/briefing_prompt.md`.
- *"Change the briefing prompt to focus more on risks."*
  — Agent edits `config/briefing_prompt.md`.

## Budget & safety (Anthropic / Claude API)

- *"What's my Claude API budget this month?"*
  — Agent reads `briefings/.usage.jsonl` and sums the current month.
- *"How much have I spent on briefings this year?"*
- *"Raise my Anthropic monthly budget to $10. Explain the tradeoff first."*
- *"Lower the minimum time between briefings to 30 minutes."*
- *"Disable AI briefings for this month."* (empties `ANTHROPIC_API_KEY`)
- *"Reset my usage ledger."* (agent should push back — see TROUBLESHOOTING.md)

## Customizing views (Phase 2+)

- *"Change the default timeframe on the Detail view to 3 months."*
- *"Show the highest-P/E stocks first in the overview table."*
  — Or just click the P/E column header in the table.
- *"Add a sector column to the overview table."*
- *"Hide the Volume column from Overview."*

## Troubleshooting

- *"The dashboard isn't loading. Figure out what's wrong."*
  — Agent reads TROUBLESHOOTING.md and runs diagnostic commands.
- *"My Finnhub key isn't being recognized. Help me debug."*
- *"Why is the news section empty?"*
- *"The price for CRDO looks wrong — investigate."*
- *"Port 8501 is already in use. What do I do?"*
- *"The AI briefing button is greyed out — why?"*
- *"I get a `.env.txt` error. Fix it for me."*

## Extending the tool

- *"Add a new tab that shows dividend history for each stock."*
- *"Add Alpha Vantage as a data source for earnings dates."*
- *"Create a separate watchlist for ETFs, distinct from my individual stocks."*
- *"Add a currency toggle so I can see prices in AED as well as USD."*
- *"Add Financial Modeling Prep as a data source."* (see APIS.md for the API directory)

## Learning the codebase (for when Roula is curious)

- *"Walk me through how a price appears on screen — from yfinance to the dashboard."*
- *"Explain how the data source cascade works, in plain English."*
- *"Show me the file I'd edit to change the dashboard's color scheme."*
- *"Explain why the Settings tab is read-only."* (§5.6 budget protection story)
- *"How does the AI briefing avoid burning through my API credits?"* (ten-item §5.6 answer)

---

**Tip.** If something above doesn't work the way it reads, tell your agent what you expected — it will diagnose and fix. This file grows as your tool grows.
