from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://postgres:root@localhost:5432/ecommerce_db"
)

def save_data(df):
    df.to_sql("transactions", engine, if_exists="replace", index=False)


# ✅ ADD THIS FUNCTION
def save_insights(results):
    df = pd.DataFrame(results, columns=["insight"])
    df.to_sql("insights", engine, if_exists="replace", index=False)