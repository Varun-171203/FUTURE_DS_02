"""FUTURE_DS_02 — RavenStack churn & revenue analysis, incl. duplicate check."""
import pandas as pd
acc=pd.read_csv("data/ravenstack_accounts.csv"); sub=pd.read_csv("data/ravenstack_subscriptions.csv")
fu=pd.read_csv("data/ravenstack_feature_usage.csv"); sup=pd.read_csv("data/ravenstack_support_tickets.csv"); ch=pd.read_csv("data/ravenstack_churn_events.csv")
for name,df,pk in [("accounts",acc,"account_id"),("subscriptions",sub,"subscription_id"),("feature_usage",fu,"usage_id"),("support_tickets",sup,"ticket_id"),("churn_events",ch,"churn_event_id")]:
    print(name, len(df), "PK duplicates:", df.duplicated(subset=[pk]).sum(), "full-row duplicates:", df.duplicated().sum())
sub=sub.drop_duplicates(subset=[c for c in sub.columns if c!="subscription_id"])  # remove 4 duplicate pairs
print("Cleaned subscriptions:", len(sub))
print("Account churn rate:", round(acc["churn_flag"].mean()*100,1), "%")
print("Churn by industry (%):"); print((acc.groupby("industry")["churn_flag"].mean()*100).round(1).sort_values(ascending=False))
print("Churn by referral (%):"); print((acc.groupby("referral_source")["churn_flag"].mean()*100).round(1).sort_values(ascending=False))
print("Recorded MRR by plan:"); print(sub.groupby("plan_tier")["mrr_amount"].sum())
print("Churn reasons:"); print(ch["reason_code"].value_counts())

# Cohort (signup quarter) retention
acc2=acc.copy(); acc2["signup_date"]=pd.to_datetime(acc2["signup_date"])
acc2["q"]=acc2["signup_date"].dt.to_period("Q").astype(str)
print("Cohort retention by signup quarter:"); print(acc2.groupby("q")["churn_flag"].agg(["count","sum","mean"]))
# Customer lifetime: signup -> first churn event
ch2=ch.copy(); ch2["churn_date"]=pd.to_datetime(ch2["churn_date"])
first=ch2.groupby("account_id")["churn_date"].min()
life=(first - acc2.set_index("account_id")["signup_date"]).dt.days
print("Median days to first churn:", life.median(), "| within 90 days %:", round((life<=90).mean()*100,1))
