import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

def analyze_data(df):
    results = []

    # -------------------------
    # BASIC CLEANING
    # -------------------------
    df = df.copy()

    df["Sales Volume"] = pd.to_numeric(df["Sales Volume"], errors="coerce")
    df = df.dropna(subset=["Sales Volume"])

    df["section"] = df["section"].astype(str).str.upper()

    # ==================================================
    # 1. TRENDING / LOW SALES (works for any dataset)
    # ==================================================
    for section in df["section"].unique():

        section_df = df[df["section"] == section]

        top_n = min(5, len(section_df))

        trending = section_df.nlargest(top_n, "Sales Volume")
        low_sales = section_df.nsmallest(top_n, "Sales Volume")

        for _, row in trending.iterrows():
            results.append({
                "section": section,
                "type": "Trending",
                "product_id": row["Product ID"],
                "product_name": row["name"],
                "sales": row["Sales Volume"]
            })

        for _, row in low_sales.iterrows():
            results.append({
                "section": section,
                "type": "Low Sales",
                "product_id": row["Product ID"],
                "product_name": row["name"],
                "sales": row["Sales Volume"]
            })

    # ==================================================
    # 2. ANOMALY DETECTION (dynamic)
    # ==================================================
    # contamination auto based on dataset size
    contamination = min(max(0.02, 5 / len(df)), 0.10)

    iso_model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    df["anomaly"] = iso_model.fit_predict(df[["Sales Volume"]])

    anomalies = df[df["anomaly"] == -1]

    for _, row in anomalies.iterrows():
        results.append({
            "section": row["section"],
            "type": "Anomaly",
            "product_id": row["Product ID"],
            "product_name": row["name"],
            "sales": row["Sales Volume"]
        })

    # ==================================================
    # 3. SALES PREDICTION (general)
    # ==================================================
    df = df.reset_index(drop=True)
    df["time_index"] = range(len(df))

    X = df[["time_index"]]
    y = df["Sales Volume"]

    lr_model = LinearRegression()
    lr_model.fit(X, y)

    future_steps = 3
    future_x = np.array([[len(df) + i] for i in range(1, future_steps + 1)])

    predictions = lr_model.predict(future_x)

    for i, pred in enumerate(predictions, start=1):
        results.append({
            "section": "ALL",
            "type": "Prediction",
            "product_id": f"future_{i}",
            "product_name": f"Future Period {i}",
            "sales": round(float(pred), 2)
        })

    # ==================================================
    # 4. SMART RECOMMENDATIONS (dynamic quartiles)
    # ==================================================
    q1 = df["Sales Volume"].quantile(0.25)
    q2 = df["Sales Volume"].quantile(0.50)
    q3 = df["Sales Volume"].quantile(0.75)

    for _, row in df.iterrows():

        sales = row["Sales Volume"]

        if sales <= q1:
            rec_type = "Heavy Discount Suggestion"

        elif sales <= q2:
            rec_type = "Promotion Suggestion"

        elif sales <= q3:
            rec_type = "Keep Price Suggestion"

        else:
            rec_type = "Price Increase Suggestion"

        results.append({
            "section": row["section"],
            "type": rec_type,
            "product_id": row["Product ID"],
            "product_name": row["name"],
            "sales": sales
        })

    return results