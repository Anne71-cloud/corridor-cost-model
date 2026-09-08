"""
volatility.py — compute realised annualised FX volatility for the Corridor Cost Model.

Replaces the illustrative volatility presets with figures you can defend,
because anyone can re-run this and get the same answer.

Method
------
    daily log return   r_t = ln(P_t / P_t-1)
    realised vol       sigma = stdev(r) * sqrt(252)

252 is the conventional number of trading days in a year. Using daily closes
rather than intraday data keeps this reproducible from free sources.

Setup (once)
------------
    pip install yfinance pandas numpy

Run
---
    python volatility.py
    python volatility.py --window 90
    python volatility.py --pairs EURZAR=X EURUSD=X

Output is a table you can read straight into the model's volatility slider,
plus a citation line to paste into the README.
"""

import argparse
from datetime import date

import numpy as np
import pandas as pd

# Yahoo Finance FX tickers. The "=X" suffix is Yahoo's convention for currency pairs.
DEFAULT_PAIRS = {
    "EURZAR=X": "EUR / ZAR  (South Africa)",
    "EURUSD=X": "EUR / USD  (offshore settlement)",
    "USDZAR=X": "USD / ZAR  (South Africa, USD leg)",
}

TRADING_DAYS = 252


def realised_vol(prices: pd.Series, window: int) -> float:
    """Annualised realised volatility, as a percentage, over the last `window` days."""
    prices = prices.dropna()
    if len(prices) < window + 1:
        raise ValueError(f"need {window + 1} observations, got {len(prices)}")

    recent = prices.iloc[-(window + 1):]
    log_returns = np.log(recent / recent.shift(1)).dropna()

    # ddof=1 -> sample standard deviation, which is the right choice for a sample of returns
    return float(log_returns.std(ddof=1) * np.sqrt(TRADING_DAYS) * 100)


def main() -> None:
    parser = argparse.ArgumentParser(description="Realised FX volatility for the corridor model.")
    parser.add_argument("--window", type=int, default=90,
                        help="lookback in trading days (default: 90)")
    parser.add_argument("--pairs", nargs="*", default=list(DEFAULT_PAIRS),
                        help="Yahoo FX tickers, e.g. EURZAR=X")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        raise SystemExit("yfinance is not installed. Run:  pip install yfinance pandas numpy")

    # Ask for extra history so the window is always fully populated after holidays.
    period = f"{max(2, args.window // 250 + 2)}y"

    print(f"\nRealised annualised volatility — {args.window} trading day window")
    print(f"Retrieved {date.today().isoformat()} from Yahoo Finance\n")
    print(f"{'Pair':<34}{'Vol':>9}")
    print("-" * 43)

    results = {}
    for ticker in args.pairs:
        label = DEFAULT_PAIRS.get(ticker, ticker)
        try:
            data = yf.download(ticker, period=period, interval="1d",
                               progress=False, auto_adjust=False)
            if data.empty:
                print(f"{label:<34}{'no data':>9}")
                continue

            closes = data["Close"]
            # yfinance returns a DataFrame when given multiple tickers; take the column.
            if isinstance(closes, pd.DataFrame):
                closes = closes.iloc[:, 0]

            vol = realised_vol(closes, args.window)
            results[ticker] = vol
            print(f"{label:<34}{vol:>8.1f}%")

        except Exception as exc:  # noqa: BLE001 - report and continue to the next pair
            print(f"{label:<34}{'error':>9}   ({exc})")

    if results:
        print("\nCitation line for the README:\n")
        print(f'  Realised {args.window}-day annualised volatility computed from daily closes, '
              f'Yahoo Finance, retrieved {date.today().strftime("%d %B %Y")}.')
        print("\nSet the model's volatility slider to the figure for your corridor.\n")


if __name__ == "__main__":
    main()
