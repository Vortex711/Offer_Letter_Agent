import pandas as pd

def load_employee_data(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Strip any whitespace
    return df
