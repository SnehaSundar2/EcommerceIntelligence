import pandas as pd

def load_data(file_path):
    try:
        # ✅ Load dataset with correct separator
        df = pd.read_csv(file_path, sep=';')

        # ✅ Strip column names (avoid hidden spaces issues)
        df.columns = df.columns.str.strip()

        print("📊 Columns found:", df.columns.tolist())

        # ✅ Ensure required columns exist
        required_cols = ['Product ID', 'Sales Volume', 'section', 'name']
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"❌ Missing column: {col}")

        # ✅ Convert Sales Volume to numeric
        df['Sales Volume'] = pd.to_numeric(df['Sales Volume'], errors='coerce')

        # ✅ Normalize section (MAN / WOMAN)
        df['section'] = df['section'].astype(str).str.upper().str.strip()

        # ✅ Clean product name
        df['name'] = df['name'].astype(str).str.strip()

        # ✅ Remove nulls
        df = df.dropna(subset=['Product ID', 'Sales Volume'])

        # ✅ Remove duplicates
        df = df.drop_duplicates(subset=['Product ID'])

        # ✅ Reset index
        df = df.reset_index(drop=True)

        print(f"✅ Cleaned dataset: {len(df)} records")

        return df

    except Exception as e:
        print("❌ Error in load_data:", str(e))
        raise