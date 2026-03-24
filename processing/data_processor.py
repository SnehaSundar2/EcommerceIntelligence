import pandas as pd

def load_data(path):
    # IMPORTANT: use separator ;
    df = pd.read_csv(path, sep=';')

    # Clean column names
    df.columns = df.columns.str.strip()

    print("Columns:", df.columns)

    return df