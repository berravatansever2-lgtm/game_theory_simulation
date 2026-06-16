import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math as m

ticker = '^GSPC'
vol = 0.1
Drift = 0.05
stock_price = 0
P1s = 1
P1c = 100
p1_util = P1s * stock_price + P1c
Market_util = -p1_util
market_data = []
p1s_data = []


def data_download(ticker, start_date, end_date):
    global vol, Drift
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    if data.empty:
        print(f"No data found for ticker {ticker}. Please check the symbol and date range.")
        return

    print("Data download complete.")
    if 'Close' not in data.columns:
        print("Error: 'Close' column not found in the downloaded data.")
        return

    original_rows = len(data)
    data = data[data['Close'] > 0]
    cleaned_rows = len(data)
    if cleaned_rows < original_rows:
        print(f"Data Cleaning: Removed {original_rows - cleaned_rows} rows with non-positive 'Close' prices.")
    if data.empty:
        print("No valid data remains after cleaning for non-positive prices.")
        return

    log_returns = np.log(data['Close']).diff().dropna()
    mu = log_returns.mean() * 252
    sigma = log_returns.std() * np.sqrt(252)

    mu_val = mu.item() if hasattr(mu, 'item') else mu
    sigma_val = sigma.item() if hasattr(sigma, 'item') else sigma

    print("\n--- Model Calibration Results ---")
    print(f"Ticker: {ticker}")
    print(f"Time Period: {start_date} to {end_date}")
    print(f"Annualized Historical Drift (μ): {mu_val:.4f} ({mu_val*100:.2f}%)")
    print(f"Annualized Historical Volatility (σ): {sigma_val:.4f} ({sigma_val*100:.2f}%)")
    vol = sigma_val
    Drift = mu_val


def market_norm(S0, vol, T, Drift):
    global stock_price
    Z = np.random.standard_normal()
    drift = (Drift - 0.5 * vol**2) * (T / 365)
    diffusion = vol * np.sqrt(T / 365) * Z
    stock_price = S0 * np.exp(drift + diffusion)
    market_data.append(stock_price)
    return stock_price


def market_down(S0, vol, T, Drift):
    global stock_price
    # Negative skew (a=-10) simulates a crash-like environment.
    Z = skewnorm.rvs(a=-10, loc=0, scale=1, size=1)[0]
    drift = (Drift - 0.5 * vol**2) * (T / 365)
    diffusion = vol * np.sqrt(T / 365) * Z
    stock_price = S0 * np.exp(drift + diffusion)
    market_data.append(stock_price)
    return stock_price


def market_up(S0, vol, T, Drift):
    global stock_price
    # Positive skew (a=10) simulates a rally-like environment.
    Z = skewnorm.rvs(a=10, loc=0, scale=1, size=1)[0]
    drift = (Drift - 0.5 * vol**2) * (T / 365)
    diffusion = vol * np.sqrt(T / 365) * Z
    stock_price = S0 * np.exp(drift + diffusion)
    market_data.append(stock_price)
    return stock_price


def player_strategy_1_sell(stock_price):
    global P1s, P1c
    # Bearish bias: more likely to sell (negative stock_num reduces holdings).
    stock_num = np.random.randint(-400, 100)
    P1s = P1s + stock_num
    P1c = P1c - stock_num * stock_price
    return P1s, P1c


def player_strategy_1_buy(stock_price):
    global P1s, P1c
    # Bullish bias: more likely to buy (positive stock_num increases holdings).
    stock_num = np.random.randint(-100, 400)
    P1s = P1s + stock_num
    P1c = P1c - stock_num * stock_price
    return P1s, P1c


def player_strategy_1_norm(stock_price):
    global P1s, P1c
    # Neutral: symmetric buy/sell range.
    stock_num = np.random.randint(-250, 250)
    P1s = P1s + stock_num
    P1c = P1c - stock_num * stock_price
    return P1s, P1c


def play_game1(S0, vol, T, Drift):
    global p1_util
    if len(market_data) == 0:
        market_norm(S0, vol, T, Drift)

    # Player reacts to the most recent price move.
    if len(market_data) > 1 and market_data[-1] > 1.1 * market_data[-2]:
        player_strategy_1_sell(stock_price)
    elif len(market_data) > 1 and market_data[-1] < 0.9 * market_data[-2]:
        player_strategy_1_buy(stock_price)
    else:
        player_strategy_1_norm(stock_price)

    # Record holdings after the trade, then let the market react to the position change.
    p1s_data.append(P1s)
    if len(p1s_data) > 1 and p1s_data[-1] > p1s_data[-2]:
        market_up(S0, vol, T, Drift)
    elif len(p1s_data) > 1 and p1s_data[-1] < p1s_data[-2]:
        market_down(S0, vol, T, Drift)
    else:
        market_norm(S0, vol, T, Drift)

    # Profit = current portfolio value minus initial capital (10000) and initial stock cost (10*10).
    p1_util = P1s * stock_price + P1c - 10000 - 10 * 10


def find_difference(stock_data):
    #Compute Pearson correlation between simulated prices and historical closes.

    stock_data = stock_data[stock_data['Close'] > 0]
    # .flatten() always returns a true 1-D array regardless of yfinance column nesting
    close_prices = stock_data['Close'].values.flatten()
    # market_data has 2 entries per day: [player-reaction price, market-reaction price, ...]
    # Take every second entry (index 1, 3, 5, ...) — the end-of-step market price.
    market_eod = market_data[1::2] #

    # Use the shorter length to avoid IndexError if counts differ slightly.
    n = min(len(close_prices), len(market_eod))
    if n < 2:
        print("Warning: Not enough data points to compute correlation.")
        return None

    xsum = ysum = xysum = xssum = yssum = 0.0
    for i in range(n):
        x = market_eod[i]
        y = float(close_prices[i])
        xsum += x
        ysum += y
        xysum += x * y
        xssum += x * x
        yssum += y * y

    numerator = n * xysum - xsum * ysum
    denominator_squared = (n * xssum - xsum**2) * (n * yssum - ysum**2)

    if denominator_squared <= 0:
        print("Warning: Cannot calculate correlation — denominator is non-positive.")
        return None

    return numerator / m.sqrt(denominator_squared)


def simulation(day_number, S0, vol, T, Drift, P1si, P1ci):
    """Run a single simulation of `day_number` trading steps.

    P1si and P1ci are passed explicitly so this function is self-contained
    and does not depend on __main__ globals.
    """
    global market_data, p1s_data, p1_util, P1s, P1c, stock_price
    # Reset all mutable state before each run.
    market_data = []
    p1s_data = []
    P1s = P1si
    P1c = P1ci
    stock_price = S0
    p1s_data.append(P1s)

    for _ in range(day_number):
        play_game1(S0, vol, T, Drift)


def monte_carlo(day_number, S0, vol, T, ticker, start_date, end_date, num_simulations, P1si, P1ci):
    data_download(ticker, start_date, end_date)
    stock_data = yf.download('^GSPC', start_date, end_date, auto_adjust=True)
    simulations = []
    r = []
    for _ in range(num_simulations):
        simulation(day_number, S0, vol, T, Drift, P1si, P1ci)
        simulations.append(p1_util)
        r.append(find_difference(stock_data))
    return simulations, r


def plot_smth(data, title="", xlabel=""):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=50, edgecolor='black', alpha=0.7)
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    plt.ylabel("Frequency")


if __name__ == "__main__":
    S0 = 10
    stock_price = 10
    P1si = 10       # initial share holdings
    P1ci = 10000    # initial cash
    T = 252         # time horizon in days (one trading year)
    vol = 0.1
    Drift = 0.05
    day_number = 252
    ticker = '^GSPC'
    start_date = '2018-01-01'
    end_date = '2018-12-31'
    num_simulations = 1000

    twovaluething = monte_carlo(
        day_number, S0, vol, T, ticker, start_date, end_date, num_simulations, P1si, P1ci
    )

    plot_smth(twovaluething[0], title="Distribution of Player Profit", xlabel="Profit")
    plt.show()
    avg = sum(twovaluething[0]) / len(twovaluething[0])
    print("Mean Profit: " + str(avg))

    # Filter out None values from correlation list (failed computations).
    valid_r = [x for x in twovaluething[1] if x is not None]
    if valid_r:
        plot_smth(valid_r, title="Distribution of Correlation (Simulated vs Historical)", xlabel="Pearson r")
        plt.show()
        avg1 = sum(valid_r) / len(valid_r)
        print("Mean Correlation: " + str(avg1))
    else:
        print("No valid correlation values to plot.")
