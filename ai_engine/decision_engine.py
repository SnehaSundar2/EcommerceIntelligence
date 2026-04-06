def analyze_data(df):
    results = []

    df['Sales Volume'] = df['Sales Volume'].astype(float)
    df['section'] = df['section'].str.upper()

    for section in ['MAN', 'WOMAN']:

        section_df = df[df['section'] == section]

        # 🔥 Trending
        trending = section_df.sort_values(by='Sales Volume', ascending=False).head(5)

        for _, row in trending.iterrows():
            results.append({
                "section": section,
                "type": "Trending",
                "product_id": row['Product ID'],
                "product_name": row['name'],
                "sales": row['Sales Volume']
            })

        # ⚠ Low Sales
        low_sales = section_df.sort_values(by='Sales Volume').head(5)

        for _, row in low_sales.iterrows():
            results.append({
                "section": section,
                "type": "Low Sales",
                "product_id": row['Product ID'],
                "product_name": row['name'],
                "sales": row['Sales Volume']
            })

    return results