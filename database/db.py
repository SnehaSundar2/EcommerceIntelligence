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

    print("Insights columns:", df.columns)  # debug

    # ✅ Save full table
    df.to_sql("insights", engine, if_exists="replace", index=False)

    # ✅ Save MEN
    if 'section' in df.columns:
        df[df['section'] == 'MAN'].to_sql("men_insights", engine, if_exists="replace", index=False)
        df[df['section'] == 'WOMAN'].to_sql("women_insights", engine, if_exists="replace", index=False)

    # ✅ Save Trending & Low Sales
    if 'type' in df.columns:
        df[df['type'] == 'Trending'].to_sql("trending_insights", engine, if_exists="replace", index=False)
        df[df['type'] == 'Low Sales'].to_sql("low_sales_insights", engine, if_exists="replace", index=False)