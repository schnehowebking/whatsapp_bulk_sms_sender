import os
import unittest
from uuid import uuid4

import pandas as pd

from contact_manager import clean_phone, is_valid_bd, load_contacts_file


TEST_TMP_DIR = os.path.join(os.path.dirname(__file__), "_tmp")


class TestContactManager(unittest.TestCase):

    def test_clean_phone_scientific_notation(self):
        self.assertEqual(clean_phone("1.712345678e+09"), "1712345678")

    def test_clean_phone_normalization(self):
        self.assertEqual(clean_phone("+880 1712345678"), "1712345678")
        self.assertEqual(clean_phone("01712345678"), "1712345678")

    def test_is_valid_bd(self):
        self.assertTrue(is_valid_bd("1712345678"))
        self.assertFalse(is_valid_bd("1212345678"))

    def test_load_contacts_file_requires_name_and_phone(self):
        os.makedirs(TEST_TMP_DIR, exist_ok=True)
        file_path = os.path.join(TEST_TMP_DIR, f"contacts_missing_{uuid4().hex}.csv")
        pd.DataFrame([{"full_name": "A", "mobile": "01712345678"}]).to_csv(
            file_path,
            index=False
        )

        with self.assertRaises(ValueError) as error:
            load_contacts_file(file_path)

        self.assertIn("Missing required column(s): name, phone", str(error.exception))

    def test_load_contacts_file_renames_columns_case_insensitive(self):
        os.makedirs(TEST_TMP_DIR, exist_ok=True)
        file_path = os.path.join(TEST_TMP_DIR, f"contacts_case_{uuid4().hex}.csv")
        pd.DataFrame([{"Name": "A", "PHONE": "01712345678"}]).to_csv(
            file_path,
            index=False
        )
        df = load_contacts_file(file_path)

        self.assertIn("name", df.columns)
        self.assertIn("phone", df.columns)
        self.assertTrue(df.iloc[0]["valid"])


if __name__ == "__main__":
    unittest.main()
