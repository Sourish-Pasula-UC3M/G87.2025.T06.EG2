import unittest
from uc3m_money.account_management_exception import  AccountManagementException
from uc3m_money.account_balance import calculate_balance
class TestCalculateBalance(unittest.TestCase):

    def test_valid_iban_and_transactions(self):
        # TC1
        self.assertTrue(calculate_balance("ES9121000418450200051332"))

    def test_valid_iban_processing_error(self):
        # TC2
        with self.assertRaises(AccountManagementException):
            calculate_balance("ES7620770024003102575766")

    def test_invalid_iban_format(self):
        # TC3
        with self.assertRaises(AccountManagementException):
            calculate_balance("INVALID_IBAN")

    def test_valid_iban_not_found(self):
        # TC4
        with self.assertRaises(AccountManagementException):
            calculate_balance("ES9820385778983000760236")

    def test_valid_iban_sum_error(self):
        # TC5
        with self.assertRaises(AccountManagementException):
            calculate_balance("ES3000491500051234567892")

    def test_valid_iban_no_transactions(self):
        # TC6
        self.assertTrue(calculate_balance("ES9820385778983000760236"))

    def test_valid_iban_large_amounts(self):
        # TC7
        self.assertTrue(calculate_balance("ES8121000418450200051332"))

if __name__ == "__main__":
    unittest.main()
