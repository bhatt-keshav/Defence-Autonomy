# EU Defense Sector System Dynamics Model — Parameter Summary

### Time Parameters

- **TIME STEP**: 0.25 (quarterly)
- **INITIAL TIME**: 0
- **FINAL TIME**: 20 (20 quarters = 5 years)
- **SAVEPER**: 0.25


## 1. Defence Spending
**Lookup (Quarterly Equipment Spending, €B)**  
^defenceSpending  
```
(1,43.03), (2,43.03), (3,43.03), (4,43.03),
(5,43.68), (6,43.68), (7,43.68), (8,43.68),
(9,44.33), (10,44.33), (11,44.33), (12,44.33),
(13,45.00), (14,45.00), (15,45.00), (16,45.00),
(17,45.67), (18,45.67), (19,45.67), (20,45.67),
(21,46.36), (22,46.36), (23,46.36), (24,46.36)
```
- 33% of total defense spending allocated to equipment.  
- EU GDP grows at 1.5% annually; defense spending = 3% of GDP.  

---

## 2. Market Share
^marketShare  
- Combined EU equipment spending (2025): €43.03 billion/quarter.  
- Rheinmetall + Thales + BAE Systems capture **30%** of this market.  
- Rheinmetall’s representative market share: **15%**.  

---

## 3. Order Backlog
^orderBacklog  
- **Initial backlog (Q1 2025)**: €63 billion  
- **Growth drivers:**  
  - New Orders = Defence Spending × Market Share = €43.03 B × 0.15 = €6.45 B / quarter  
  - Orders Fulfilled = Backlog × Delivery Rate  
- **Backlog evolution (example)**  
  - Q1 2025: 66.935 B  
  - Q4 2025: 74.339 B  
- **Target range 2025–2030:** ~€63 B → €118 B (CAGR ≈ 13.5%)  

---

## 4. Delivery Rate
^deliveryRate  
Quarterly delivery fraction of backlog, growing 5% annually:

| Year | Quarters | Delivery Rate (%) |
|------|-----------|------------------|
| 2025 | Q1–Q4 | 4.00 |
| 2026 | Q5–Q8 | 4.20 |
| 2027 | Q9–Q12 | 4.41 |
| 2028 | Q13–Q16 | 4.63 |
| 2029 | Q17–Q20 | 4.86 |
| 2030 | Q21–Q24 | 5.10 |

- Conservative 5% annual growth reflects gradual capacity expansion.  
- Equivalent annual backlog fulfillment ≈ 14–16%.  

---

## 5. Revenue
^revenue  
- Derived from Orders Fulfilled = Backlog × Delivery Rate.  
- **Q1 2025 example:**  
  - Backlog = 63 B; Delivery Rate = 4% → Revenue = €2.52 B.  
- **2025 total revenue:** ≈ €10.99 B (consistent with 35–40% growth).  
- Revenue grows with delivery rate improvements to €2.9 B/quarter by 2030.  

---

## 6. Working Capital Ratio
^workingCapital  
- Typical range (European defense firms): **1.5 – 2.0**  
- Rheinmetall baseline: **1.86**  
- Simplified approximation:  
  ```
  ΔWorkingCapital = OrderBacklog × 0.175
  ```  

---

## 7. Costs
From **SD Model_Grok.md → Operating Expenses** section.  
- Operating Expenses = **84.8% of Revenue**  
- Operating Margin = **15.2%**

### Breakdown by Category (% of Revenue)
| Category | % | Sub-components | Sub-% of Revenue |
|-----------|---|----------------|-----------------|
| **Production Costs** | 48.5 | Structural Metals | 11.5 |
| | | Critical Materials | 5.3 |
| | | Energy | 8.0 |
| **Other Operating Expenses** | 34.8 | Personnel | 20.5 |
| | | R&D | 4.9 |
| | | Overhead | 6.7 |
| **Miscellaneous Costs** | 1.5 | — | 1.5 |

Example (Q1 2025, Revenue €1.95 B):  
- Operating Expenses €1.6536 B  
- Operating Profit €296.4 M  
- NOPAT (20–30% tax): €207–237 M  

---

### Formula Summary
```
NewOrders = DefenceSpending × MarketShare
OrdersFulfilled = OrderBacklog × DeliveryRate
Backlog(t) = Backlog(t−1) + NewOrders − OrdersFulfilled
Revenue = OrdersFulfilled
OperatingExpenses = Revenue × 0.848
OperatingProfit = Revenue − OperatingExpenses
NOPAT = OperatingProfit × (1 − TaxRate)
FreeCashFlow = NOPAT − Investment − ΔWorkingCapital
ΔWorkingCapital = OrderBacklog × 0.175
```

---

### Initial Conditions (t = 0, Q1 2025)
| Variable | Symbol | Value |
|-----------|---------|-------|
| Order Backlog | B₀ | €63 B |
| Cash Reserves | C₀ | €2 B |
| Defence Spending | D₀ | €43.03 B / quarter |
| Market Share | s | 15% |
| Delivery Rate | δ | 4.0% |
| Working Capital Ratio | w | 1.86 |
| Operating Margin | m | 15.2% |
