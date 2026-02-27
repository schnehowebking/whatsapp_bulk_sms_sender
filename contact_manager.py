import pandas as pd
from database import add_contact

def import_csv(file_path):
    df = pd.read_csv(file_path)

    if "name" not in df.columns or "phone" not in df.columns:
        raise Exception("CSV must contain name and phone columns")

    for _, row in df.iterrows():
        name = str(row["name"])
        phone = str(row["phone"])
        add_contact(name, phone)