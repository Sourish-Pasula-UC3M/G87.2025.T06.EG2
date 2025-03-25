import unittest
import os
import json
from uc3m_money.account_deposit import deposit_into_account
from uc3m_money.account_management_exception import AccountManagementException

class TestDepositIntoAccount(unittest.TestCase):

    def setUp(self):
        # Set up a temporary JSON file for each test
        self.test_file = "test_deposit.json"

    def tearDown(self):
        # Clean up the test file after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def write_test_file(self, content):
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    def test_valid_deposit(self):
        content = {"IBAN": "ES9121000418450200051332", "AMOUNT": "EUR 2500.00"}
        self.write_test_file(content)
        sig = deposit_into_account(self.test_file)
        self.assertIsInstance(sig, str)
        self.assertGreater(len(sig), 0)

    def test_file_not_found(self):
        with self.assertRaises(AccountManagementException):
            deposit_into_account("nonexistent.json")

    def test_invalid_json_format(self):
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("not a json")
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_missing_fields(self):
        content = {"IBAN": "ES9121000418450200051332"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_invalid_iban(self):
        content = {"IBAN": "INVALID_IBAN", "AMOUNT": "EUR 100.00"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_invalid_currency(self):
        content = {"IBAN": "ES9121000418450200051332", "AMOUNT": "USD 100.00"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_amount_above_limit(self):
        content = {"IBAN": "ES9121000418450200051332", "AMOUNT": "EUR 15000.00"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_amount_below_zero(self):
        content = {"IBAN": "ES9121000418450200051332", "AMOUNT": "EUR -100.00"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

    def test_invalid_amount_format(self):
        content = {"IBAN": "ES9121000418450200051332", "AMOUNT": "EUR one hundred"}
        self.write_test_file(content)
        with self.assertRaises(AccountManagementException):
            deposit_into_account(self.test_file)

if __name__ == "__main__":
    unittest.main()
