# Game-Theoretic Simulation of Stock Market Investor Strategies

**Author:** Berra Vatansever | **Date:** August 2025

---

## Overview

This research models financial markets as a **two-player zero-sum game** between an investor and the market. Using Geometric Brownian Motion (GBM) and Monte Carlo simulation (1,000 runs × 252 trading days), it tests how different investor risk-aversion strategies affect profitability across varying market volatility regimes.

Historical data from S&P 500, Tesla, Amazon, Microsoft, Nvidia, Apple, and Google was sourced via `yfinance`, calibrated for 2008 and 2018 market conditions.

The full research paper is included in this repository: [A Game Theoretical Approach to Stock Prices and Investor Strategies in Financial Markets (PDF)](./A%20Game%20Theoretical%20Approach%20to%20Stock%20Prices%20and%20Investor%20Strategies%20in%20Financial%20Markets.pdf)

---

## Research Questions

- Can a game-theoretic framework simulate real-world stock price behavior?
- How does investor risk aversion affect profitability in low vs. high volatility markets?

---

## Methodology

### Game Structure

- 2-player zero-sum game: investor vs. market
- 3 rounds per iteration: market move → investor action → market response
- Investor utility: `Stock Price × Shares Held + Cash`
- Market utility: negative of investor profit

### Mathematical Models

- **Geometric Brownian Motion (GBM)** for stochastic price generation
- **Monte Carlo simulation** for distributional analysis of outcomes across 1,000 game repetitions

### Investor Types Tested

| Type | Strategy | Trigger Threshold |
|------|----------|------------------|
| 1 (Standard) | Buy/sell on moderate price change | ±10% |
| 2 (Risk Averse) | Buy/sell on large moves only | ±30% |
| 3 (Risk Taking) | React to smallest changes | ±1% |
| 4 (Inactive) | Only acts on large moves, stays idle otherwise | ±30%, no random trading |

---

## Key Findings

- The GBM-based game-theoretic model **failed to replicate real stock prices** (mean correlation coefficient ≈ 0.001 across 1,000 simulations for the S&P 500, confirmed across 7 stocks and indices). This result is expected: GBM generates a distribution of possible price paths, not a single predictive trajectory. The near-zero correlation reflects the model's stochastic nature rather than a flaw in its construction.

- **Investor responsiveness, not volatility regime, drives profitability.** Type 3 (reacts to ±1% changes) consistently outperformed all other strategies in both low (5%) and high (80%) volatility environments, earning an average profit of ~$19,800 vs. ~$14,000 for the standard player and ~$900 for the most risk-averse player.

- **Crisis-period calibration (2008) reduced average investor profit significantly vs. stable periods (2018)**, consistent with the increased uncertainty and unpredictability of returns during financial crises. Higher volatility compressed the investor's expected profit from ~$140,000 to ~$9,400 in the 2008 regime.

- Results are structurally consistent with **Kyle (1985)'s model of informed trading**, where faster information processing and quicker strategic adaptation generate persistent excess returns — the foundational theoretical basis for modern high-frequency trading.

---

## Limitations

- **Zero-sum assumption:** Real financial markets are not zero-sum — they create and destroy value through economic activity. This simplification limits the model's realism.
- **Single action per day:** The investor is constrained to one buy/sell decision per trading day. Real markets allow continuous trading.
- **Rational agents only:** The model assumes fully rational investors. Incorporating behavioural noise (irrational decisions, herd behaviour) would produce more realistic dynamics.
- **No Nash equilibrium analysis:** The game structure is defined but the equilibrium strategies are not formally solved. A natural extension would derive the Nash equilibrium investor strategy given the market's GBM response function.
- **GBM limitations:** GBM assumes constant drift and volatility and fails to capture jump processes, fat tails, and volatility clustering observed in real markets.

---

## Future Work

The natural Version 2 of this model would incorporate three improvements:

1. **Formal Nash equilibrium derivation** — solve for the equilibrium investor strategy given the market's information structure
2. **Kyle (1985) information framework** — replace the ad hoc market response function with a formal model where the market maker updates prices based on observed order flow, distinguishing informed from noise traders
3. **Relaxing the zero-sum assumption** — model the market as a positive-sum game where aggregate returns reflect economic growth, with the investor capturing a share through strategic positioning

---

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python simulation.py
```

---

## Dependencies

| Library | Purpose |
|---------|---------|
| numpy | Vectorised numerical computation |
| pandas | Data manipulation |
| yfinance | Historical market data |
| matplotlib | Visualisation |
| scipy | Statistical functions |

---

## References

- Kyle, A. S. (1985). Continuous auctions and insider trading. *Econometrica*, 53(6), 1315–1335.
- Evangelista, D., Saporito, Y., & Thamsten, Y. (2022). Price formation in financial markets: a game-theoretic perspective. *arXiv*.
- Hannafey, K. (2021). Modeling the Stock Market Through Game Theory. *Georgia Southern Commons*.
- Rapoport, A., & Chammah, A. M. (1965). *Prisoner's Dilemma*. University of Michigan Press.
