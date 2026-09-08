# The Corridor Cost Model

An interactive model of what it actually costs to move money between Europe and Africa.

The advertised rate is not the cost. Spread, correspondent fees, settlement delay and unhedged FX exposure across the float are all cost, and only one of them appears on the invoice. This tool separates them and shows what a payment loses end to end.

**Live:** https://corridor-cost-model.netlify.app
**Built by:** Saranne Ndamba — treasury and financial management across South Africa and the DRC, MSc Finance and Investment Management (University of Salford)

---

## What it does

Move any slider and the model decomposes a single cross-border payment into four parts:

| Component | What it is |
|---|---|
| Reaches the beneficiary | What actually lands on the other side |
| FX spread | The margin away from interbank mid |
| Fixed fees | Sending bank, correspondent hops, beneficiary deductions |
| Cost of the delay | The financing cost of money in flight |

It also reports a **1σ unhedged exposure** figure — the FX movement you are carrying across the settlement window — and annualises the total at your payment frequency.

---

## The arithmetic

All of it, so you can check the method rather than trust it:

```
spread_cost  = amount × spread_bps ÷ 10,000
fee_cost     = fixed_fees
delay_cost   = amount × cost_of_capital × days ÷ 365
all_in_cost  = spread_cost + fee_cost + delay_cost
all_in_pct   = all_in_cost ÷ amount × 100

exposure_1σ  = amount × annual_volatility × √(days ÷ 365)
```

### Stated simplifications

Two, both of which make the model **conservative** rather than flattering:

1. **Delay cost uses simple, not compound, interest.** This understates the cost slightly at long delays.
2. **The exposure figure assumes returns are roughly normal** over a short window. Thin-market currencies have fatter tails than that, so treat the 1σ number as a floor, not a ceiling.

The exposure figure is a **range being carried, not a cost**. Roughly two thirds of outcomes fall inside the band and one third outside it.

---

## Where the numbers come from

| Input | Source | Status |
|---|---|---|
| FX volatility | Realised annualised volatility from daily closes (Yahoo Finance), computed as `stdev(log returns) × √252` | Reproducible — see `volatility.py` |
| Cost of capital | South African Reserve Bank published prime rate, used as a stated proxy | Public |
| FX spread | Published bank tariff sheets; World Bank Remittance Prices Worldwide decomposes cost into fee and FX margin per corridor | Public |
| Fixed fees | Published bank tariff sheets | Public |
| Settlement delay | SWIFT gpi published statistics | Public |

### Corridor presets are illustrative

The corridor dropdown loads a starting volatility, spread and delay so the model has somewhere to begin. **These are illustrative, not measurements, and should not be quoted as such.** Every one of them is meant to be overridden with your own figures.

### Benchmark evidence on the page

All figures in the evidence panel are from the World Bank's *Remittance Prices Worldwide*:

- Cost of sending $200 to Sub-Saharan Africa averaged **8.78%** in Q1 2025, against a **6.49%** global average — the most expensive receiving region in the world
- **Three in four** SSA corridors cost over 10%; only two came in under the 3% SDG target, against 25 globally
- **Nine of the thirteen** costliest corridors worldwide originate in Sub-Saharan Africa (Q3 2025); South Africa remains the most expensive G20 country to send from
- Average cost of sending from **France rose to 5.23%** (Q3 2025) from 5.14% a year earlier, while the G8 average fell from 5.99% to 5.40%

**Important caveat, stated on the page as well:** remittance data is not corporate trade payment data. The two price differently. These figures are included because they are the best public measure of how this corridor behaves and because they establish the direction of travel — not because they transfer directly to a commercial payment.

---

## What the model deliberately leaves out

Frictions from the operating side that a calculator cannot price, and which are frequently larger than the spread:

- Repeat KYC and documentary checks on counterparties already onboarded, re-triggered by each payment
- Correspondent banks withdrawing from a corridor with little notice, forcing a rebuild of the payment route
- Payments held for compliance review with no visibility on when they will clear
- Stock sitting at port while funds are in flight, converting a treasury delay into a commercial one
- The cost of holding buffer balances in a weak currency purely to absorb timing risk

---

## Running it

It's a single HTML file with no dependencies, no build step and no tracking.

```bash
# locally
open index.html

# or serve it
python3 -m http.server 8000
```

Deployed via Netlify from this repository. Edit `index.html`, commit, and it redeploys automatically.

`volatility.py` is separate and optional — it computes the realised volatility figures used as inputs.

---

## Companion research

*From Education to Equity: How Allan Gray's Ecosystem Builds and Funds Black Entrepreneurs in South Africa* — an MSc dissertation on why capital fails to reach African entrepreneurs.

Access and movement are one question at two scales. This model is the second half.

---

## Corrections welcome

If the method is wrong, I would rather know. Open an issue or email me — that is more useful than agreement.

saranne.ndamba@outlook.com · [LinkedIn](https://www.linkedin.com/in/sarannendamba)

© Saranne Ndamba, 2026
