from kafka_module.producer import send_event

def analyze_data(df):
    results = []

    # Trending products
    trending = df.sort_values(by='Sales Volume', ascending=False).head(5)

    for _, row in trending.iterrows():
        event = f"Product {row['Product ID']} is trending (Sales: {row['Sales Volume']})"
        send_event("trending", event)
        results.append(event)

    # Low sales products (FIXED)
    low_sales = df.sort_values(by='Sales Volume').head(5)

    for _, row in low_sales.iterrows():
        event = f"Low sales for product {row['Product ID']} (Sales: {row['Sales Volume']})"
        send_event("low_sales", event)
        results.append(event)

    return results