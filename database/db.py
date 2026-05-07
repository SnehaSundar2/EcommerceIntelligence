from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://postgres:root@localhost:5432/ecommerce_db"
)

def save_data(df):
    df.to_sql("transactions", engine, if_exists="replace", index=False)


def save_insights(results):

    if not results:
        print("No insights to save ❌")
        return

    df = pd.DataFrame(results)

    print("Insights columns:", df.columns)
    print("Insight types:\n", df['type'].value_counts())

    # =========================
    # MAIN TABLE
    # =========================
    df.to_sql("insights", engine, if_exists="replace", index=False)

    # =========================
    # SECTION TABLES
    # =========================
    if 'section' in df.columns:
        df[df['section'] == 'MAN'].to_sql(
            "men_insights", engine, if_exists="replace", index=False
        )

        df[df['section'] == 'WOMAN'].to_sql(
            "women_insights", engine, if_exists="replace", index=False
        )

    # =========================
    # TRENDING / LOW SALES
    # =========================
    if 'type' in df.columns:

        df[df['type'] == 'Trending'].to_sql(
            "trending_insights", engine, if_exists="replace", index=False
        )

        df[df['type'] == 'Low Sales'].to_sql(
            "low_sales_insights", engine, if_exists="replace", index=False
        )

    # =========================
    # ANOMALIES
    # =========================
    df[df['type'] == 'Anomaly'].to_sql(
        "anomaly_insights", engine, if_exists="replace", index=False
    )

    # =========================
    # PREDICTIONS
    # =========================
    df[df['type'] == 'Prediction'].to_sql(
        "prediction_insights", engine, if_exists="replace", index=False
    )

    # =========================
    # ALL RECOMMENDATIONS
    # =========================
    recommendation_types = [
        'Heavy Discount Suggestion',
        'Promotion Suggestion',
        'Keep Price Suggestion',
        'Price Increase Suggestion'
    ]

    df[df['type'].isin(recommendation_types)].to_sql(
        "recommendation_insights",
        engine,
        if_exists="replace",
        index=False
    )

    # =========================
    # SUMMARY TABLE
    # =========================
    summary = df.groupby('type').size().reset_index(name='count')

    summary.to_sql(
        "insights_summary",
        engine,
        if_exists="replace",
        index=False
    )

    print("✅ Insights saved successfully!")