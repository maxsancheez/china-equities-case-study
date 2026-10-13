"""Compare China ETFs against the S&P 500: YTD return, 1-year return, max drawdown."""
import datetime as dt

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

TICKERS = ["MCHI", "FXI", "KWEB", "ASHR", "SPY"]
REEL_DATE = "2026-07-21"


def max_drawdown(series: pd.Series) -> float:
    return (series / series.cummax() - 1).min()


def main():
    end = dt.date.today()
    start = end - dt.timedelta(days=3 * 365)
    prices = yf.download(TICKERS, start=start, end=end, auto_adjust=True)["Close"].dropna()

    year_start = prices[prices.index >= f"{end.year}-01-01"].iloc[0]
    one_year_ago = prices[prices.index >= str(end - dt.timedelta(days=365))].iloc[0]
    at_reel = prices[prices.index >= REEL_DATE].iloc[0]
    last = prices.iloc[-1]

    summary = pd.DataFrame({
        "YTD %": (last / year_start - 1) * 100,
        "1Y %": (last / one_year_ago - 1) * 100,
        "Since reel %": (last / at_reel - 1) * 100,
        "Max DD (3Y) %": prices.apply(max_drawdown) * 100,
    }).round(1)
    print(summary.to_string())
    summary.to_csv("summary.csv")

    (prices / prices.iloc[0] * 100).plot(figsize=(10, 5), title="Growth of 100 (3Y)")
    plt.axvline(pd.Timestamp(REEL_DATE), color="gray", linestyle="--", label="Reel posted")
    plt.legend()
    plt.tight_layout()
    plt.savefig("growth.png", dpi=150)


if __name__ == "__main__":
    main()
