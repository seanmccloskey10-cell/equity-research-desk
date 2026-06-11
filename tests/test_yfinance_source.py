"""Smoke test — verify yfinance actually returns data for one ticker.

This test hits the real network. It's a smoke test, not a unit test.
Skip if offline.
"""

from __future__ import annotations

import pytest

from data_sources.yfinance_source import YFinanceSource


@pytest.fixture(scope="module")
def source():
    return YFinanceSource()


def test_is_configured(source):
    assert source.is_configured() is True


def test_get_quote_live(source):
    q = source.get_quote("AAPL")
    if q is None:
        pytest.skip("yfinance unavailable (offline or rate-limited)")
    assert q["ticker"] == "AAPL"
    assert isinstance(q["price"], float)
    assert q["price"] > 0
    assert q["source"] == "yfinance"


def test_get_history_live(source):
    df = source.get_history("AAPL", period="1mo", interval="1d")
    if df is None or df.empty:
        pytest.skip("yfinance history unavailable")
    for col in ("Open", "High", "Low", "Close", "Volume"):
        assert col in df.columns


def test_get_fundamentals_live(source):
    f = source.get_fundamentals("AAPL")
    if f is None:
        pytest.skip("yfinance fundamentals unavailable")
    assert f["ticker"] == "AAPL"
    assert f["source"] == "yfinance"


def test_get_quote_bad_ticker(source):
    q = source.get_quote("XXXXXXXXXXX_NOT_A_REAL_TICKER")
    assert q is None


def test_dividend_yield_is_decimal_fraction_not_percent(source):
    """Accuracy-critical: dividend_yield MUST be a fraction (e.g. 0.0232 for 2.32%).

    yfinance 0.2.40+ changed `dividendYield` to percent units. This test locks
    in the normalization so a future yfinance bump can't silently break UI
    displays that multiply by 100. If this fails, QQQI's dividend would render
    as 1504% instead of 15%.
    """
    f = source.get_fundamentals("JNJ")
    if f is None or f.get("dividend_yield") is None:
        pytest.skip("yfinance unavailable or JNJ returned no dividend")
    dy = f["dividend_yield"]
    # JNJ pays roughly 2-4%. A fraction value sits in [0.01, 0.06]. A percent
    # value would be in [1, 6]. If we're accidentally returning percent, this
    # catches it.
    assert 0.001 < dy < 0.20, (
        f"JNJ dividend_yield={dy} is out of sanity range for a fraction. "
        f"Likely unit convention regression — expected ~0.02-0.04 (i.e. 2-4%)."
    )


def test_high_yield_etf_dividend_normalized(source):
    """A high yielder's dividend must STILL be stored as a fraction (e.g. 0.06 for
    6%), never a percent (6.0) — this guards the normalization at the upper end,
    not just for ~2-4% payers.

    yfinance's data for any single niche ticker can lapse (QQQI used to report
    ~15% and now returns near-zero), so we try several reliably-reported high
    yielders and use the first that has usable data; skip only if none do.
    """
    candidates = ["MO", "T", "VZ", "QQQI"]  # Altria / AT&T / Verizon ~5-7%
    dy = used = None
    for ticker in candidates:
        f = source.get_fundamentals(ticker)
        if f and f.get("dividend_yield") and f["dividend_yield"] > 0.04:
            dy, used = f["dividend_yield"], ticker
            break
    if dy is None:
        pytest.skip("yfinance returned no usable high-yield dividend data")
    # A fraction sits well under 1; a percent value (5-7) would blow past 0.50.
    assert 0.04 < dy < 0.50, (
        f"{used} dividend_yield={dy} out of fraction range — likely a "
        f"percent-vs-fraction normalization regression."
    )


def test_roe_is_decimal_fraction(source):
    """ROE should be a fraction too (0.15 for 15%), not a percent."""
    f = source.get_fundamentals("KO")
    if f is None or f.get("roe") is None:
        pytest.skip("yfinance unavailable or KO missing ROE")
    roe = f["roe"]
    # KO has been between 0.20 and 0.50 historically. Percent would be 20-50.
    assert -2.0 < roe < 3.0, (
        f"KO ROE={roe} out of fraction range. "
        f"If this is in percent units, the UI would show 2000% instead of 20%."
    )
