# FUTURE_DS_02 — SaaS Churn & Revenue Analytics (RavenStack)

**Future Interns | Data Science & Analytics — Task 2**
**Intern:** Piyush Saxena

## Problem
RavenStack is a (synthetic) SaaS startup. Using 5 linked tables, this project investigates what drives churn, support load and revenue before public launch.

## Dataset — RavenStack Synthetic SaaS Dataset
Credit: **River @ Rivalytics** (MIT-like licence, fully synthetic, no PII). Source README is included as `DATASET_README.md`.
- accounts — 500 rows
- subscriptions — 5,000 rows (4,996 after cleaning, see below)
- feature_usage — 25,000 rows
- support_tickets — 2,000 rows
- churn_events — 600 rows

## Data Quality / Duplicate Check (done first)
- Full-row duplicates: **0 in all 5 tables**
- Primary keys unique in accounts, subscriptions, support_tickets, churn_events; **0 FK orphans** in any table
- feature_usage: 21 `usage_id` values are reused for *different* events (ID collisions, 42 rows) — rows kept, usage_id not used as a key
- subscriptions: **4 duplicate pairs** identical in every field except subscription_id ($8,544 MRR double-count) — one copy of each removed: 5,000 → **4,996**
- Expected nulls kept: subscription end_date (active plans), satisfaction_score (no response), churn feedback_text (no comment)

## Key Findings
- Account churn is **22.0%** (110/500). Churn events cover 352 unique accounts — most reactivated, so the two numbers are different measures.
- **Industry matters:** DevTools churns at 31.0%, Cybersecurity at 16.0%.
- **Channel matters:** event-acquired accounts churn at 30.2%, partner-acquired at 14.6%.
- Plan tier, trial, billing frequency, auto-renew, seats, ticket volume and usage show **almost no difference** between churned and retained accounts.
- **Revenue concentration:** Enterprise = 34% of subscriptions but **75% of recorded MRR** ($8.47M of $11.33M cleaned).
- Top churn reasons: features (19.0%), budget (17.3%), support (17.3%). 20.5% of churn followed a recent upgrade.
- Support: urgent tickets resolve in 34.6h vs 36.4h for low priority — priority barely changes anything. Satisfaction averages 3.98/5.
- Beta features are no more error-prone than stable ones (0.56 vs 0.57 errors/event).

## Cohort & Lifetime Analysis (per the official Task 2 brief)
- **Cohorts by signup quarter:** retention improves from 70.9% (2023 Q1) to 85.0% (2024 Q4) — with the caveat that newer cohorts have had less time to churn.
- **Cohorts by plan:** retention is flat (Basic 78.0%, Pro 78.1%, Enterprise 77.9%).
- **Customer lifetime:** median time to first churn event is **82 days** (mean 133); **53.4% of first churns occur within 90 days**, 91.8% within the first year. Ended subscriptions last a median of 42 days.
- **Retention trend:** monthly active subscription records grew from 3 (Jan 2023) to 4,703 (Dec 2024).
- Key implication: retention effort belongs in the **first 90 days** — onboarding and early check-ins, not late win-back.

## Files
- `FUTURE_DS_02_SaaS_Churn_Revenue_Analytics_Report.pdf` — full report
- `FUTURE_DS_02_RavenStack_Dashboard.xlsx` — Excel dashboard incl. Duplicate_Check sheet
- `analysis.py` — reproducible analysis incl. the duplicate check
- `data/` — the 5 source CSVs

## Run
```bash
pip install pandas openpyxl matplotlib
python analysis.py
```
