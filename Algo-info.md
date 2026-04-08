# Algorithm Information - In Simple Terms

This document explains all the algorithms used in the Dynamic Pricing System in easy-to-understand language.

---

## 1. LSTM (Long Short-Term Memory) - The Demand Predictor

### What is it?
LSTM is like a super-smart memory system that can remember patterns from the past and use them to predict the future.

### Real-World Analogy
Imagine you run an ice cream shop. You notice:
- Ice cream sales go UP in summer
- Sales go DOWN in winter
- Sales spike on weekends
- Sales drop during exams (students don't come out)

LSTM is like writing all this in a diary and using it to guess how much ice cream you'll sell next week. It remembers patterns and uses them to predict.

### How It Works (Simple Steps)

```
Step 1: Collect past sales data (last 30 days)
        Example: Day 1: 50 units, Day 2: 45 units, Day 3: 60 units...

Step 2: Find patterns
        - Does Monday always sell less?
        - Does beginning of month sell more?

Step 3: Remember important things, forget unimportant ones
        - Remember: "Weekends = More sales"
        - Forget: "Random Tuesday with low sales due to rain"

Step 4: Predict future demand
        "Based on patterns, next Monday will sell ~55 units"
```

### Why Use LSTM?

| Feature | Benefit |
|---------|---------|
| Long-term memory | Remembers seasonal patterns (Diwali sales, summer demand) |
| Short-term memory | Tracks recent trends (last week was slow) |
| Pattern recognition | Finds hidden patterns humans might miss |

### Example
Product: Running Shoes
- Last 7 days sales: 10, 12, 8, 15, 20, 22, 18
- LSTM sees: "Sales increasing, weekend coming"
- Prediction: "Next 3 days will sell approximately 25, 28, 24 units"

---

## 2. Reinforcement Learning (RL) - The Learning Price Setter

### What is it?
RL is like training a dog with treats. The system tries different prices, gets "rewards" when it makes more money, and learns which prices work best.

### Real-World Analogy
Think of a new shopkeeper learning pricing:
- Day 1: Sets price at ₹100 → Sells 50 items → Good reward!
- Day 2: Raises price to ₹150 → Sells 10 items → Bad reward!
- Day 3: Sets price at ₹110 → Sells 45 items → Good reward!

Over time, the shopkeeper learns: "₹100-110 is the sweet spot"

### The ε-Greedy Strategy (Exploration vs Exploitation)

```
ε (epsilon) = 20% exploration rate

This means:
- 80% of the time: Use the BEST known price (Exploitation)
- 20% of the time: Try a NEW random price (Exploration)
```

### Why Both Exploration and Exploitation?

| Strategy | What it does | Problem if only this |
|----------|--------------|----------------------|
| Exploitation | Use what works | Might miss better prices |
| Exploration | Try new things | Might lose money on experiments |
| Both (80-20) | Best of both worlds | Optimal balance |

### How Q-Learning Works (Simple Version)

```
Q = Quality Score for each price option

Example for a T-shirt (base price ₹500):

Price Option    | Q-Value (Score) | Meaning
----------------|-----------------|------------------
₹350 (0.7x)     | 45              | Low profit per sale
₹400 (0.8x)     | 62              | Moderate
₹450 (0.9x)     | 78              | Good balance
₹500 (1.0x)     | 85              | Best performer ✓
₹550 (1.1x)     | 70              | Some resistance
₹600 (1.2x)     | 50              | Too expensive
₹650 (1.3x)     | 30              | Very few buyers
```

The system picks ₹500 most often because it has the highest Q-value (85).

### Learning Process

```
1. TRY a price
2. OBSERVE the result (sales, revenue)
3. CALCULATE reward
   Reward = (Revenue this time - Last revenue) / Last revenue × 100
4. UPDATE Q-value for that price
5. REPEAT and get smarter over time
```

---

## 3. Price Elasticity - The Sensitivity Calculator

### What is it?
Price elasticity measures how much customers care about price changes. Some products can handle price increases; others can't.

### Real-World Analogy

**Medicine (Low Elasticity)**
- Price goes up 10% → People still buy it (they need it)
- Demand drops only 2%

**Fashion Item (High Elasticity)**
- Price goes up 10% → People stop buying
- Demand drops 25%

### The Formula (Simplified)

```
Elasticity = (% Change in Sales) ÷ (% Change in Price)

Example:
- You raised price from ₹100 to ₹110 (10% increase)
- Sales dropped from 100 units to 85 units (15% decrease)
- Elasticity = -15% ÷ 10% = -1.5
```

### What Elasticity Numbers Mean

| Elasticity | Type | Meaning | Example Products |
|------------|------|---------|------------------|
| 0 to -1 | Inelastic | Price doesn't affect demand much | Medicine, Salt, Petrol |
| -1 | Unit Elastic | Equal effect | Some services |
| -1 to -∞ | Elastic | Price greatly affects demand | Luxury items, Fashion |

### How We Use It

```
If elasticity = -0.5 (inelastic):
   → Safe to increase price slightly
   → Customers won't leave

If elasticity = -2.0 (elastic):
   → Be careful with price increases
   → Consider discounts to boost sales
```

---

## 4. Contextual Bandit - The Smart Chooser

### What is it?
Like a gambler who gets smarter about which slot machine to play based on the time of day, crowd size, etc.

### Real-World Analogy
You sell umbrellas at different prices:

| Situation | Best Price Strategy |
|-----------|---------------------|
| Sunny day | Lower price (₹150) to attract buyers |
| Rainy day | Higher price (₹300) - people need it |
| Monsoon season | Premium price (₹350) |
| Winter (no rain) | Heavy discount (₹100) |

The Contextual Bandit learns which situation needs which price.

### Context = Situation

The system considers:
```
1. Demand Level: High / Medium / Low
2. Inventory: Lots / Normal / Little
3. Competition: Cheaper / Same / Expensive than us
4. Season: Festival / Normal / Off-season
```

### How It Chooses

```
Current Context:
- Demand: HIGH
- Inventory: LOW
- Competition: HIGHER than us
- Season: FESTIVAL

System thinks: "High demand + Low stock + Festivals = INCREASE PRICE"
Action: Apply 1.15x multiplier (15% price increase)
```

---

## 5. Dynamic Pricing Engine - The Master Calculator

### What is it?
The brain that combines all algorithms and real-time data to set the final price.

### Factors Considered

| Factor | Weight | What it Measures |
|--------|--------|------------------|
| Demand | 25% | How fast is the product selling? |
| Searches | 20% | How many people are searching for it? |
| Cart Additions | 20% | How many added to cart (but didn't buy)? |
| Views | 15% | How many people are looking? |
| Concurrent Users | 15% | How many viewing RIGHT NOW? |
| Inventory | 5% | How much stock do we have? |

### Decision Logic (Simplified)

```
IF searches are HIGH + carts are HIGH + inventory is LOW:
   → People want this product!
   → INCREASE price by 10-15%

IF searches are LOW + no carts + inventory is HIGH:
   → Product not moving
   → DECREASE price by 5-10%
```

### Example Calculation

```
Product: Wireless Earbuds
Base Price: ₹2000

Real-time Data:
- Searches (24h): 45 (+10% signal)
- Views (24h): 80 (+10% signal)
- Cart additions: 25 (+15% signal)
- Concurrent users: 8 (+5% signal)
- Sales velocity: Good (+5% signal)
- Inventory: 50 units (Normal, 0%)

Total Multiplier = 1 + (0.10×0.25 + 0.10×0.15 + 0.15×0.20 + 0.05×0.15)
                 = 1 + (0.025 + 0.015 + 0.03 + 0.0075)
                 = 1.0775 ≈ 1.08

New Price = ₹2000 × 1.08 = ₹2160
```

---

## Summary: How All Algorithms Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                    DYNAMIC PRICING SYSTEM                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [LSTM Forecaster] ──→ Predicts: "Tomorrow's demand = 50"  │
│         ↓                                                   │
│  [Price Elasticity] ─→ Calculates: "Elasticity = -1.2"     │
│         ↓                                                   │
│  [RL Agent] ────────→ Suggests: "Use 1.1x multiplier"      │
│         ↓                                                   │
│  [Context Analysis] ─→ Confirms: "High demand context"     │
│         ↓                                                   │
│  [Dynamic Engine] ──→ Final Price: ₹1100 (from ₹1000)      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **LSTM** = Remembers the past to predict the future
2. **Reinforcement Learning** = Learns from trial and error
3. **Price Elasticity** = Understands customer sensitivity
4. **Contextual Bandit** = Makes decisions based on current situation
5. **Dynamic Engine** = Combines everything for the final price

The beauty is that these algorithms work together, constantly learning and improving, just like an experienced shopkeeper who gets better at pricing over years of experience - except this system learns in days, not years!
