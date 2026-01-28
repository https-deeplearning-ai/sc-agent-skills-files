---
name: analyzing-marketing-campaign
description: Analyze weekly marketing campaign performance data across channels. Use when analyzing multi-channel digital marketing data to calculate funnel metrics (CTR, CVR) and compare to benchmarks, compute cost and revenue efficiency metrics (ROAS, CPA, Net Profit), or get budget reallocation recommendations based on performance rules.
---

# Marketing Campaign Analysis

Automated analysis of multi-channel marketing campaign data from BigQuery.

## Data Source

Query data from BigQuery using the `bigquery:execute_sql` tool.

**Location:** `marketing-analytics-483823.marketing.campaign_performance`

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Campaign date |
| campaign_name | STRING | Campaign identifier |
| channel | STRING | Marketing channel |
| segment | STRING | Customer segment |
| impressions | INTEGER | Ad impressions (NULL for Email) |
| clicks | INTEGER | Number of clicks |
| conversions | INTEGER | Number of conversions |
| spend | FLOAT | Marketing spend in dollars |
| revenue | FLOAT | Revenue generated in dollars |
| orders | INTEGER | Number of orders |

## Required Input

The user must specify a week to analyze. Accept formats like:
- "Dec 9-15" or "December 9-15, 2024"
- "2024-12-09 to 2024-12-15"
- "week of Dec 9" or "last week"

If the date range is ambiguous, ask the user to clarify before querying.

## Querying Data

Always filter by date range—never pull the entire table. Example query structure:

```sql
SELECT
  channel,
  SUM(impressions) as impressions,
  SUM(clicks) as clicks,
  SUM(conversions) as conversions,
  SUM(spend) as spend,
  SUM(revenue) as revenue,
  SUM(orders) as orders
FROM `marketing-analytics-483823.marketing.campaign_performance`
WHERE date BETWEEN '2024-12-09' AND '2024-12-15'
GROUP BY channel
```

Adjust the query as needed for the specific analysis (e.g., group by segment, include daily breakdown).

## Data Quality Check

1. Check for NULL values (Email channel won't have impressions)
2. Verify no negative values in numeric columns
3. Flag anomalies (e.g., conversions without clicks)

## Funnel Analysis

Calculate per channel:

- **Click Through Rate (CTR)** = clicks / impressions × 100
- **Conversion Rate (CVR)** = conversions / clicks × 100

Compare to user-provided benchmarks, report difference in percentage points. If benchmarks not provided, use:

| Channel | CTR | CVR |
|---------|-----|-----|
| Facebook_Ads | 2.5% | 3.8% |
| Google_Ads | 5.0% | 4.5% |
| TikTok_Ads | 2.0% | 0.9% |
| Email | 15.0% | 2.1% |

## Efficiency Analysis

Calculate per channel:

- **Return On Ad Spend (ROAS)** = revenue / spend
- **Cost Per Acquisition (CPA)** = spend / conversions
- **Net Profit** = revenue - Total Costs
  - Total Costs = spend + (orders × Shipping Cost) + (revenue × Product Cost %)
  - Defaults: Shipping Cost = $8/order, Product Cost = 35% of revenue

Compare to user-provided targets. Defaults:
- **Target ROAS**: 4.0x minimum
- **Max CPA**: $50

## Output Format

Present results as tables with status indicators:

**Funnel Analysis Table:**
| Channel | CTR Actual | CTR Benchmark | CTR Diff | CVR Actual | CVR Benchmark | CVR Diff |

**Efficiency Analysis Table:**
| Channel | ROAS | Status | CPA | Status | Net Profit | Status |

Status indicators:
- ROAS: "[OK] Above" if >= target, "[X] Below" if < target
- CPA: "[OK] Below" if <= max, "[X] Above" if > max
- Net Profit: "[OK] Positive" if > 0, "[X] Negative" if <= 0

Follow each table with brief channel-by-channel interpretation.

## Budget Reallocation

If user asks about budget reallocation, read `references/budget_reallocation_rules.md` for the complete decision framework including eligibility rules, performance-based actions, and constraints.
