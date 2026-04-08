import pandas as pd
import os
import re


def clean_phone(phone):

    phone = str(phone).strip()

    if "E+" in phone or "e+" in phone:
        phone = "{:.0f}".format(float(phone))

    phone = phone.replace(".0", "")
    phone = phone.replace("+", "")
    phone = phone.replace(" ", "")

    if phone.startswith("880"):
        phone = phone[3:]

    if phone.startswith("0"):
        phone = phone[1:]

    return phone


def is_valid_bd(phone):

    pattern = r"^1[3-9][0-9]{8}$"

    return re.match(pattern, phone)


def load_contacts_file(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path, dtype=str)

    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path, dtype=str)

    else:
        raise ValueError("Unsupported file. Use .csv, .xls, or .xlsx")

    normalized_columns = {column.strip().lower(): column for column in df.columns}
    required = ["name", "phone"]
    missing = [column for column in required if column not in normalized_columns]
    if missing:
        missing_columns = ", ".join(missing)
        raise ValueError(f"Missing required column(s): {missing_columns}")

    # Rename user-provided columns (e.g. Name/PHONE) to canonical names.
    df = df.rename(columns={
        normalized_columns["name"]: "name",
        normalized_columns["phone"]: "phone",
    })

    df["phone"] = df["phone"].apply(clean_phone)

    df = df.drop_duplicates(subset=["phone"])

    df["valid"] = df["phone"].apply(lambda x: bool(is_valid_bd(x)))

    return df
