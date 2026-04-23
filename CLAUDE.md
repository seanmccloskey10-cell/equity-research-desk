# CLAUDE.md — in-project agent guide

**You are Claude Code running in Roula's cloned copy of this repo.** This file teaches you how the codebase is organized, what the non-negotiable rules are, and how to extend the tool safely. Read [PRD.md](PRD.md) for full product context, then come back here.

**Session-start reading order:** this file → [SESSION-NOTES.md](SESSION-NOTES.md) (recent changes, unusual state, open threads) → [PRD.md](PRD.md) if you need the full spec.

---

## What this project is

A local-first equity research dashboard. Python + Streamlit + Plotly. Runs on Roula's laptop, displays live data for her watchlist (default: CRDO, HIMS, BABA, QQQI, IREN). yfinance is the primary data source — **the tool works with zero API keys.**

---

## Who the user is

**Roula.** Senior business professional at GE, based in Dubai. Fluent with Claude Cowork. **Not technically savvy** — she operates this tool via natural-language prompts to you. She does not type commands, edit `.env` by hand, or debug stack traces. Your job is to be the translation layer between her intent and the code.

She is on **Windows 11** — see the Windows gotchas section below.

She does not like crypto. No crypto examples, data, or demo tickers.

---

## Non-negotiable rules

These are load-bearing. Breaking them undoes safety properties Sean explicitly designed in.

1. **The Settings tab is READ-ONLY.** [views/settings.py](views/settings.py) displays key status and copyable prompts. It **never writes to `.env`**. All `.env` mutations happen through you (the agent), not through the Streamlit UI. Reason: the Anthropic monthly-budget hard cap (PRD §5.6 #5) only works if the UI cannot raise the cap on its own.

2. **All Anthropic API calls live in [views/briefing.py](views/briefing.py) — nowhere else.** Do not import `anthropic` anywhere else in the codebase. The briefing module exists so budget protection (PRD §5.6, all ten items) can be enforced in one audit-able location.

3. **No background calls to Anthropic, ever.** The Claude call must fire only from the explicit button-click confirmation inside the briefing module. Not on `st.rerun()`. Not on page load. Not on navigation. If you're editing `views/briefing.py`, re-read PRD §5.6 first.

4. **Never commit `.env`.** `.gitignore` excludes it; keep it that way. Keys in source files = automatic reject.

5. **Project is self-contained.** Do not read from or write to personal directories on the host machine from inside the app. Any data the app needs lives under the project root.

---

## The `run.py` wrapper

Everything Python-related in this project goes through `python run.py <cmd>`. It handles venv creation, dependency install, and cross-platform path issues so Roula's experience is one consistent command regardless of OS state.

| Command | What it does |
|---|---|
| `python run.py setup` | Create `.venv` if missing, install `requirements.txt`, copy `.env.example` → `.env` if missing, run `setup_check.py` |
| `python run.py start` | Start the dashboard (spawns streamlit, writes `.streamlit.pid`) |
| `python run.py stop` | Kill the streamlit process (reads `.streamlit.pid`) |
| `python run.py test` | Run pytest |
| `python run.py shell` | Print the venv Python path — useful if you need to run ad-hoc Python inside the project's environment |

**Do not tell Roula to run `pip install`, `python -m venv`, or `streamlit run`.** Those are `run.py`'s job. If you need a new package, add it to `requirements.txt` and tell her to run `python run.py setup` — the deps marker will trigger a reinstall.

If Python 3.11+ or Git is missing from her machine, see the **Bootstrap** section in [README.md](README.md) — install via `winget` before reaching for `run.py`.

---

## Code map

```
equity-research-desk/
├── run.py                  One-command wrapper — venv + deps + dispatch
├── app.py                  Streamlit entry — tab registry + sidebar
├── setup_check.py          First-run validator + monthly Anthropic spend reporter
├── scripts/
│   ├── start_dashboard.py  Spawns streamlit run, writes .streamlit.pid
│   └── stop_dashboard.py   Reads .streamlit.pid, kills the process
├── config/
│   ├── tickers.yaml        Watchlist — edit to add/remove tickers
│   ├── settings.py         Loads .env + tickers into a typed Settings object
│   ├── theme.py            Colors (stub in Phase 1, expanded in Phase 2)
│   └── briefing_prompt.md  Editable prompt template for the AI briefing (Phase 4)
├── data_sources/
│   ├── base.py             DataSource ABC — normalized return shapes
│   ├── yfinance_source.py  Primary source, no key (Phase 1 — fully implemented)
│   ├── finnhub_source.py   Secondary (Phase 3 — stub)
│   ├── alphavantage_source.py  Tertiary (Phase 3 — stub)
│   └── orchestrator.py     Cascades calls across sources in priority order
├── views/
│   ├── overview.py         Watchlist table — live prices
│   ├── ticker_detail.py    Per-ticker detail with dropdown selector
│   ├── comparison.py       Side-by-side view (Phase 3 — stub)
│   ├── briefing.py         AI briefing (Phase 4 — stub; ONLY place anthropic is imported)
│   └── settings.py         READ-ONLY status + copyable prompts
├── components/
│   ├── metric_card.py      st.metric wrapper with delta coloring
│   ├── sparkline.py        Plotly mini-chart (Phase 2)
│   └── candlestick_chart.py  Plotly OHLCV chart (Phase 2)
├── lib/
│   ├── formatting.py       Money / percent / volume formatters
│   ├── cache.py            Streamlit cache TTL wrappers
│   ├── timeframes.py       Shared period/interval tuples (1D .. 5Y)
│   ├── market_hours.py     NYSE session classifier (sidebar indicator)
│   ├── budget.py           Anthropic usage ledger + rate-limit + cost math
│   └── briefing_engine.py  Context builder + SOLE Anthropic call site
├── briefings/              AI briefings land here (gitignored .md + .usage.jsonl)
└── tests/                  Smoke tests — orchestrator cascade + yfinance fetch
```

### Data flow

```
config/tickers.yaml → config/settings.py (load_settings)
                                │
                                ▼
                       app.py (creates Settings + Orchestrator, caches them)
                                │
                                ▼
                        views/*.py (render(settings, orch))
                                │
                                ▼
           orchestrator.py._cascade() → yfinance_source.get_quote()
                                             (or next source if None)
```

---

## Conventions

- **File names:** `lowercase_with_underscores.py`. Docs at project root are `UPPERCASE.md`; docs elsewhere are `lowercase.md`.
- **Type hints** on all public functions. `from __future__ import annotations` at the top of every Python module.
- **Normalized data shapes.** Every `DataSource` method returns the shape documented in [data_sources/base.py](data_sources/base.py). Views never branch on which source produced a value.
- **Caching.** Use the wrappers in [lib/cache.py](lib/cache.py), not raw `st.cache_data`. TTLs are centralized there.
- **Formatting.** Use [lib/formatting.py](lib/formatting.py) helpers. Never `f"${value:.2f}"` inline.
- **No business logic in `app.py`.** It is the tab registry and sidebar. Views do the work.

---

## Extension patterns

### Add a new ticker

Edit [config/tickers.yaml](config/tickers.yaml). Append under `tickers:`:

```yaml
  - symbol: TSLA
    name: Tesla
    note: EV / energy
```

Tell the user to hit the Refresh button in the sidebar. No code change required.

### Add a new data source

1. Create `data_sources/<name>_source.py`.
2. Subclass `DataSource` from [data_sources/base.py](data_sources/base.py). Implement `is_configured`, `get_quote`, `get_fundamentals`, `get_history`, `get_company_info`. Optionally `get_news`, `get_earnings`.
3. Match the return shapes documented in `base.py` so views stay source-agnostic.
4. Register in [data_sources/orchestrator.py](data_sources/orchestrator.py) → `build_default_orchestrator()`, in priority order.
5. Add the API key to [.env.example](.env.example) with a comment explaining what it unlocks.
6. Add a smoke test in `tests/test_<name>_source.py`.

### Add a new view / tab

1. Create `views/<name>.py` exposing `render(settings, orch) -> None`.
2. Import in [app.py](app.py) and add a tab in the `st.tabs([...])` list.
3. Copy the shape of [views/overview.py](views/overview.py) — small, one-purpose.
4. Use existing `components/` and `lib/formatting.py` helpers.

### Add a component

1. Create `components/<name>.py` with a function taking data and either returning a Plotly figure or rendering Streamlit directly.
2. Plotly for charts, Streamlit primitives for UI.

### Change theme / styling

Edit [config/theme.py](config/theme.py) and [.streamlit/config.toml](.streamlit/config.toml). Theme helpers available:
- `apply_theme()` — inject the global CSS (called once from `app.py`).
- `page_header(title, subtitle)` — consistent tab-level heading with an accent underline. Use instead of `st.header`.
- `section_label(text)` — small-caps sub-section label with a left accent tick. Use instead of `st.markdown("**Label**")` between an `st.subheader` and a metric-card grid.

### Add or update an API key

**Through the agent only.** The Settings tab is read-only by design. Flow:
1. Open `.env` in VS Code.
2. Set the value: `FINNHUB_API_KEY=<value>`.
3. Tell the user to restart the dashboard (`python scripts/stop_dashboard.py && python scripts/start_dashboard.py`) or hit Refresh in the sidebar.
4. Optionally: `python setup_check.py` to verify the key is detected.

---

## When to ask the user first

Before any of these, confirm with Roula:

- Changing the default theme or the sidebar layout
- Raising `ANTHROPIC_MONTHLY_BUDGET_USD` — explain the tradeoff first
- Modifying `views/briefing.py` in a way that touches the cost-control flow
- Removing a data source she already configured
- Deleting or renaming a view she's been using
- Any change that would require her to reconfigure keys she's already set

---

## What not to do

- Do not import `anthropic` anywhere except `views/briefing.py`
- Do not write to `.env` from any Streamlit component
- Do not add background jobs, timers, or `st.rerun()` calls that could trigger Anthropic calls
- Do not hardcode API keys in source files
- Do not commit `.env`, `briefings/*.md`, or `.streamlit.pid`
- Do not add crypto tickers or demo examples (Roula does not like crypto)
- Do not add browser-fetched data or client-side JavaScript (CORS was the previous build's failure mode — PRD §12.2)

---

## Windows gotchas

- **Hidden `.txt` extension.** `.env` may be saved as `.env.txt` by Notepad. [setup_check.py](setup_check.py) detects this explicitly. Fix: rename, or copy `.env.example` via CLI.
- **Forward slashes in Python.** Use `pathlib.Path`. Never hardcode backslashes.
- **`pip` not on PATH.** Fall back to `py -m pip install -r requirements.txt`.
- **`taskkill` vs `kill`.** Handled inside [scripts/stop_dashboard.py](scripts/stop_dashboard.py) — reference that pattern if you need to kill other processes.

## Why [.vscode/settings.json](.vscode/settings.json) is committed

VS Code's Python extension auto-injects `.env` variables into every integrated terminal session when `python.terminal.useEnvFile` is on. We turn this OFF deliberately. Reasons:

1. **Consistency.** Enabling injection would make the app behave one way in the VS Code terminal and a different way in plain PowerShell. For a non-technical user, that's a debugging trap.
2. **Secret scoping.** Injection would expose `ANTHROPIC_API_KEY` (and any other secret) to every shell command Roula runs. We want secrets scoped to the Python process that actually needs them.
3. **We already handle `.env` in Python.** [config/settings.py](config/settings.py) calls `load_dotenv()` at import time — that's the single source of truth.

Side benefit: VS Code no longer shows the "environment file is configured but terminal environment injection is disabled" notification to Roula on first open.

---

## Additional data sources worth considering (future)

See [APIS.md](APIS.md) for the full directory of financial APIs Roula can evaluate — organized by problem (market data, news, fundamentals, macro, earnings, filings, insider/institutional, options, alternative). Includes recommendations, free-tier limits, paid tier pricing, and a decision framework. Sean's top-3 picks:

1. **Financial Modeling Prep** — deep fundamentals. Free 250/day, $19/mo unlimited.
2. **FRED** (St. Louis Fed) — unlimited free macro data.
3. **Quartr** — earnings call transcripts; also a Claude Cowork connector.

The non-API honest flag: **Koyfin** ($35/mo web dashboard) is the zero-build alternative if she'd rather not iterate on this tool. Don't recommend switching by default — tell her it exists if she asks about visual-quality benchmarks.

When Roula asks to add a new API, follow the "Add a new data source" pattern above and the walkthrough at the bottom of APIS.md.

---

## Phase status (keep this synced with reality)

- **Phase 0** — scaffold: ✅ shipped
- **Phase 1** — yfinance MVP: ✅ shipped
- **Phase 2** — candlestick + sparkline + theme polish: ✅ shipped
  - Custom CSS injection in `config/theme.py` (typography, metric-card borders, tabular numerics, tab styling)
  - Candlestick + volume subplot in `components/candlestick_chart.py` with up/down-colored volume bars
  - 7 timeframe toggles on Detail view (1D / 5D / 1M / 3M / 6M / 1Y / 5Y); 1D + 5D use intraday intervals
  - Inline sparkline column on Overview table (30-day close prices via `st.column_config.LineChartColumn`)
  - Loading spinners during data fetches
  - Shared `lib/timeframes.py` so every view aligns on period/interval tuples
- **Phase 3** — Finnhub + Alpha Vantage + Comparison tab: ✅ shipped
  - `data_sources/finnhub_source.py` — quote, fundamentals, company info, news (last 7 days, 10 articles max), earnings (next 90 days, earliest event); history intentionally skipped (paid-tier)
  - `data_sources/alphavantage_source.py` — quote, fundamentals, company info; rate-limit response (`Note`/`Information`) correctly returns None so cascade moves on
  - `views/comparison.py` — 5-axis radar (Market Cap / P/E inv / P/B inv / ROE / Div Yield, min-max normalized), YTD bar chart, raw-metrics table
  - `views/ticker_detail.py` — real news + earnings panels when Finnhub key is present; same "add key to unlock" fallback when not
  - `lib/cache.py` — added `cache_news` (10 min) and `cache_earnings` (6 hr) wrappers
  - All cascades handle missing keys cleanly — dashboard works identically whether 0, 1, 2, or 3 optional keys are configured
- **Phase 4** — AI Briefing + all ten §5.6 budget items: ✅ shipped
  - `lib/budget.py` — usage ledger, month-total, rate-limit math, Sonnet 4.6 pricing constants
  - `lib/briefing_engine.py` — context builder, prompt loader, SOLE Anthropic call site (`generate_briefing`)
  - `views/briefing.py` — full UI with all ten §5.6 safeguards enforced structurally (no-key gate → cache display → hard-cap gate → rate-limit gate → cost-disclosed button → `st.dialog` confirmation → ledger-then-cache write)
  - `ANTHROPIC_API_KEY` never touches any module outside `lib/briefing_engine.py`
  - `st.dialog` requires Streamlit ≥ 1.32 — pinned in requirements.txt
  - Briefings cached at `briefings/YYYY-MM-DD.md`; usage log at `briefings/.usage.jsonl`; both gitignored
- **Phase 5** — docs completion: ✅ shipped
  - [PROMPTS.md](PROMPTS.md) expanded: AI-briefing prompts, budget management, troubleshooting, extending the tool
  - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) covers setup, dashboard lifecycle, API keys, AI-briefing gates, Windows-specific issues
  - Every phase's code is cross-referenced here in CLAUDE.md
- **Phase 6** — fresh-clone smoke test on a separate Windows folder: pending
- **Phase 10** — Full visual redesign + KaTeX bug fix + AI Brief per-section renderer + rename: ✅ shipped (2026-04-22)
  - **Rename**: tool is now "Roula's Equity Research Desk" — page title ([app.py](app.py) `st.set_page_config`), sidebar title, and module docstring. Project-level docs (README, PRD) intentionally left unchanged (builder-side)
  - **New theme primitives** in [config/theme.py](config/theme.py):
    - `page_header(title, subtitle)` — tab-level heading with accent underline rule
    - `section_label(text, icon=None, tone="accent")` — small-caps label, optional icon chip, tone keyword (`accent` / `gain` / `loss` / `warn` / `cool` / `purple` / `muted`) colors the left tick + icon tint + heading text
    - `callout(body, tone, icon, heading)` — hero-style tinted card for punch-line moments (replaces generic `st.info` where visual weight is warranted)
  - **Sidebar rebuilt** in [app.py](app.py): flat text lines → bordered watchlist cards with colored left border tied to day direction, NYSE status pill with pulse animation when open (`@keyframes erd-pulse`), data-source chip rows with role tags. Price font color later fixed from muted grey → primary text at 0.9rem/500-weight after Sean flagged it was hard to read
  - **Detail tab** ([views/ticker_detail.py](views/ticker_detail.py)) full rewrite: flat 10-card wall → hero strip (Price · Market Cap · P/E · Dividend Yield · 52W Position) + section-labeled groups with tones/icons (Price history 📉 · Trading activity ⚡ · 52-week range 📏 · About 🏢 · Recent news 📰 · Upcoming earnings 🗓). News and earnings items live in `st.container(border=True)`. About expander defaults to open
  - **All views** now use `page_header` + `section_label` consistently; each sub-section has a tone + optional icon. Analysis sub-sections (Valuation / Profitability / Balance sheet & risk) use tones without icons to keep the 3-group rhythm cohesive. Settings sub-sections get icons + tones throughout
  - **AI Brief per-section renderer** — new [lib/briefing_render.py](lib/briefing_render.py) parses the briefing body by `### ` headings, classifies each (TL;DR / Snapshot / Themes / Risk / Earnings / Questions), emits custom HTML cards with per-section styling (accent gradient hero for TL;DR, amber warning tint for Risk, numbered chip-cards for Questions, elevated table for Earnings, custom `→` bullets for Themes). Uses `markdown` lib (added to [requirements.txt](requirements.txt), tables extension enabled)
  - **KaTeX `$...$` math-mode bug fixed** — new `escape_streamlit_dollars(text)` helper in [lib/formatting.py](lib/formatting.py). Streamlit's `st.markdown` / `st.write` / `st.caption` run through markdown-it-py with a math plugin that interprets `$...$` as inline LaTeX. Briefings, news summaries, and company descriptions with `$CRDO` or `$189.49` were rendering as italic serif math. Applied escape at every user/LLM-text display site. For the briefing (pre-rendered HTML), `$` is replaced with `&#36;` HTML entity after markdown→HTML conversion
  - **Metric card height consistency** — rows with mixed-delta cards (Price has `+3.37%` chip, Market Cap doesn't) were ragged. Fixed in [config/theme.py](config/theme.py): `[data-testid="stMetric"]` is now a flex column with `min-height: 124px` and `margin-top: auto` on `stMetricDelta` to pin to the bottom. Spacer div added under 52W High/Low cards in Analysis to match peer-rank-bar vertical footprint. Earnings container's nested metrics swapped for compact labelled text to avoid 300px container inflation
  - **Patterns tab** ([views/patterns.py](views/patterns.py)) — spline smoothing on price traces, consistent font family, tighter title positioning
  - **Tests**: 171 → **196 green** (+8 new [tests/test_formatting.py](tests/test_formatting.py) for `escape_streamlit_dollars`, +17 new [tests/test_briefing_render.py](tests/test_briefing_render.py) for section classification, splitting, HTML shape, dollar-entity escaping, markdown bolds, tables)
  - **New dependency**: `markdown>=3.5` pinned in `requirements.txt`
  - Invariants still holding: `import anthropic` only in `lib/briefing_engine.py` + test; Settings tab READ-ONLY; no Anthropic background calls; briefing render pipeline is pure display-time HTML transformation
- **Phase 9** — Paid-tool UI patterns ported (hero strip, grouped sections, peer-rank bars): ✅ shipped
  - [components/peer_rank_bar.py](components/peer_rank_bar.py) — Koyfin-style compact horizontal bar replacing the `Peer median: X` text caption. Shows watchlist min→max with a dot at the ticker's position; dot is color-coded green/amber/red by direction-aware percentile (direction flag: `higher_is_better` is True for ROE/margin, False for P/E/D/E, None for neutral like market cap/beta). Pure HTML/CSS via `st.markdown` — one `st.plotly_chart` per metric × ten metrics would have hammered render time
  - [views/analysis.py](views/analysis.py) — hero strip at top (ticker+name, price+change, market cap, P/E, dividend yield, RSI, 52W position — all dense in one row). Fundamentals split into three purpose-based sections: **Valuation** (MC, P/E TTM, Forward P/E, P/B, Div Yield), **Profitability** (ROE, Profit Margin, EPS), **Balance Sheet & Risk** (D/E, Beta, 52W High, 52W Low). Every peer-comparable metric gets a rank bar; cross-ticker-tricky metrics (EPS, Beta) render neutral
  - [views/overview.py](views/overview.py) — explicit section subheaders (`Markets` / `Your watchlist` / `Biggest mover today`). Same content, clearer framing as a dashboard vs a scroll
  - Test count 156 → 171: new [tests/test_peer_rank_bar.py](tests/test_peer_rank_bar.py) (15 tests covering `_position_pct`, `_goodness` direction logic, `_dot_color` thresholds, degenerate-range handling)
  - Research: surveyed Koyfin, Bloomberg Terminal, TradingView, FinChat for UI patterns. Deliberately skipped full widget customization, multi-panel Bloomberg density, fake TTM/Q/Annual period toggles, command palette, and third-party Streamlit deps — each would add complexity without matching Roula's usage
- **Phase 8** — UI polish + Analysis per-stock rewrite + data provenance + briefing v4: ✅ shipped
  - Tab nav CSS reworked: padded, button-like labels with hover + active-state borders (in [config/theme.py](config/theme.py))
  - [lib/provenance.py](lib/provenance.py) — `SOURCE_DESCRIPTIONS` catalogue + `render_footer(orch)` caption. Sidebar data-sources section upgraded to show each source's role + what it covers + cost. Footer caption appended under every live-data tab
  - [views/patterns.py](views/patterns.py) rewritten as a 2-column grid — all 5 charts visible at once, details behind a compact expander per card (was: expander-only, forced to click each)
  - [data_sources/yfinance_source.py](data_sources/yfinance_source.py) — `get_fundamentals` extended with `forward_pe`, `eps`, `beta`, `profit_margin`, `debt_to_equity` (normalized to ratio from percent-multiple). Base shape in [data_sources/base.py](data_sources/base.py) updated accordingly
  - [views/analysis.py](views/analysis.py) rewritten: **per-stock** deep dive instead of watchlist-wide radar. Ticker selector → fundamentals grid (10 metrics: market cap, PE TTM, forward PE, P/B, dividend yield, ROE, profit margin, debt/equity, EPS, beta) with a **peer-median caption under each card** for context. Technicals section unchanged. `_min_max_norm`, `_invert_norm`, `_ytd_return_pct`, radar and YTD-bar helpers all removed
  - [lib/briefing_engine.py](lib/briefing_engine.py) — context payload extended with the new fundamentals fields. `PROMPT_VERSION` → `v4-2026-04-21`. [config/briefing_prompt.md](config/briefing_prompt.md) schema block updated to document the new fields and their unit conventions (decimal vs ratio)
  - Test count went 154 → 156: new [tests/test_provenance.py](tests/test_provenance.py) (4), rewritten [tests/test_analysis.py](tests/test_analysis.py) (6), extended [tests/test_briefing_engine.py](tests/test_briefing_engine.py) (+2 v4 assertions). [tests/test_app_boots.py](tests/test_app_boots.py) updated to assert the Patterns grid layout
- **Phase 7** — Analysis tab (Fundamentals + Technicals) + Patterns (Educational) tab + briefing v3: ✅ shipped
  - Tab order is now Overview · Detail · AI Brief · Analysis · Patterns (Educational) · Settings (highest-priority surfaces first per the tool's owner)
  - `lib/technicals.py` — pure-pandas RSI(14, Wilder), MACD(12/26/9), SMA(20/50/200), crossover detection, `price_vs_ma`. No new dependency (no ta-lib / pandas-ta)
  - `views/analysis.py` replaces `views/comparison.py`. Two stacked sections in one tab:
    - **Fundamentals** (top, full watchlist) — radar + YTD bars + metrics table ported verbatim from the retired comparison view
    - **Technicals** (bottom, per-ticker dropdown) — RSI/MACD/crossover/price-vs-200MA metric cards, 90-day RSI sparkline, MA overlay chart (price + SMA 20/50/200)
  - `views/patterns.py` — educational reference library. 5 patterns (Head & Shoulders, Double Top, Cup & Handle, Flag/Pennant, Ascending Triangle) built on synthesized price data with annotated Plotly charts + "what / means / fails" text. Explicitly NOT a watchlist scanner; the tab banner says so
  - `lib/briefing_engine.py` — `build_watchlist_context` extended to parallel-fetch 1-year history and compute a `technicals` subdict per ticker. `PROMPT_VERSION` bumped `v2-2026-04-21` → `v3-2026-04-21` and the constant is written into briefing frontmatter
  - `config/briefing_prompt.md` — added accuracy rules #6 (technical-indicator citation discipline) and #7 (fundamentals-lead-technicals-support framing) plus the per-ticker payload schema so Claude sees unit conventions explicitly
  - "AI Briefing" header + tab label renamed to "AI Brief" (tighter, matches user's preferred vocab)
  - `views/comparison.py` + `tests/test_comparison.py` deleted — normalization helpers and their tests migrated to `views/analysis.py` + `tests/test_analysis.py` with the same math
  - Test count went 124 → 154: new `test_technicals.py` (20), `test_analysis.py` (9), `test_patterns.py` (4), `test_briefing_engine.py` (+4 v3 assertions), `test_app_boots.py` updated for 6-tab layout. Invariants still hold: `import anthropic` only in `lib/briefing_engine.py` + its test

### Additional hardening (shipped beyond the phase plan)

- **[tests/test_app_boots.py](tests/test_app_boots.py)** — AppTest-based smoke tests (5) that render the live app + click through every tab, catching view-level regressions
- **[lib/market_hours.py](lib/market_hours.py)** — NYSE session indicator in the sidebar (`🟢 Open` / `🟡 Pre-market` / `🟡 After-hours` / `🔴 Closed`)
- **Budget meter** turns amber when spend crosses 80% of monthly cap, warning proactively before the hard cap disables the button
- **Anthropic SDK timeout** pinned at 90s (default was 10 minutes — too long for an interactive UI)
- **Ledger/cache write failures** treated as non-fatal: briefing still displayed, but a warning prompts manual spend recording (Anthropic has already charged at that point)
- **YAML provenance frontmatter** on every cached briefing (`generated_at`, `model`, `input_tokens`, `output_tokens`, `cost_usd`, `watchlist`). Download button serves the full file; UI strips the frontmatter before rendering
- **Overview sorting fix**: numeric columns are raw floats with `NumberColumn` so sort-by-market-cap works numerically, not lexically
- **Last-refreshed timestamp** in sidebar so data staleness is visible at a glance
- **Yfinance-down banner** in Overview when every ticker fails to fetch — beats a table of em dashes
- **Ticker input normalization**: `" tsla "` and `"TSLA"` resolve identically; duplicates in `tickers.yaml` are deduped on load

When you ship work, update this section.
