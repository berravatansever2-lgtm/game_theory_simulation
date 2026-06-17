# Game-Theoretic Simulation of Stock Market Investor Strategies

**Author:** Berra Vatansever | **Date:** August 2025

---

## Overview

This research models financial markets as a **two-player zero-sum game** 
between an investor and the market. Using Geometric Brownian Motion (GBM) 
and Monte Carlo simulation (1,000 runs × 252 trading days), it tests how 
different investor risk-aversion strategies affect profitability across 
varying market volatility regimes.

Historical data from S&P 500, Tesla, Amazon, Microsoft, Nvidia, Apple, 
and Google was sourced via `yfinance`, calibrated for 2008 and 2018 
market conditions.

---

## Research Questions

- Can a game-theoretic framework simulate real-world stock price behavior?
- How does investor risk aversion affect profitability in low vs. 
  high volatility markets?

---

## Methodology

**Game Structure**
- 2-player zero-sum game: investor vs. market
- 3 rounds per iteration: market move → investor action → market response
- Investor utility: `Stock Price × Shares Held + Cash`
- Market utility: negative of investor profit

**Mathematical Models**
- Geometric Brownian Motion (GBM) for stochastic price generation
- Monte Carlo simulation for distributional analysis of outcomes

**Investor Types Tested**

| Type | Strategy | Trigger Threshold |
|------|----------|-------------------|
| 1 (Standard) | Buy/sell on price change | ±10% |
| 2 (Risk Averse) | Buy/sell on large moves only | ±30% |
| 3 (Risk Taking) | React to smallest changes | ±1% |
| 4 (Inactive) | Only acts on large moves, stays idle otherwise | ±30%, no random trading |

---

## Key Findings

- The GBM-based game theoretical model **failed to replicate real stock 
  prices** (mean correlation coefficient ≈ 0.001 across 1,000 simulations 
  for S&P, confirmed across 7 stocks/indices).
- **Investor responsiveness, not volatility regime, drives profitability.** 
  Type 3 (reacts to ±1% changes) outperformed all others in both low 
  (5%) and high (80%) volatility environments.
- Results are consistent with the working principle behind 
  **high-frequency trading**: faster strategic adaptation → higher returns.
- Crisis-period calibration (2008) reduced average investor profit 
  significantly vs. table periods (2018), consistent with the increased risk during financial crises.
