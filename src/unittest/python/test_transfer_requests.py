import unittest
import re
from uc3m_money.transfer_request import transfer_request

VALID_IBAN = "ES9121000418450200051332"
VALID_IBAN_2 = "ES9820385778983000760236"
def is_valid_md5(s):
    return isinstance(s, str) and re.fullmatch(r'[a-fA-F0-9]{32}', s) is not None

class TestTransferRequest(unittest.TestCase):

    def test_TC1_valid_transfer(self):
        result = transfer_request(VALID_IBAN, VALID_IBAN_2, "text valid", "ORDINARY", "01/01/2026", 10.00)
        self.assertTrue(is_valid_md5(result))

    def test_TC2_valid_urgent_transfer(self):
        result = transfer_request(VALID_IBAN, VALID_IBAN_2, "text is valid", "URGENT", "02/02/2049", 10.01)
        self.assertTrue(is_valid_md5(result))

    def test_TC3_valid_immediate_high_amount(self):
        result = transfer_request(VALID_IBAN, VALID_IBAN_2, "text validdddddddddddddddddd", "IMMEDIATE", "30/11/2025", 9999.99)
        self.assertTrue(is_valid_md5(result))

    def test_TC4_valid_ordinary_max_amount(self):
        result = transfer_request(VALID_IBAN, VALID_IBAN_2, "text validddddddddddddddddddd", "ORDINARY", "31/12/2050", 10000.00)
        self.assertTrue(is_valid_md5(result))

    def test_TC5_valid_small_transfer(self):
        result = transfer_request(VALID_IBAN, VALID_IBAN_2, "text validddddddddddddddddddd", "ORDINARY", "31/12/2050", 15.20)
        self.assertTrue(is_valid_md5(result))

    def test_TC6_invalid_from_iban_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("15", VALID_IBAN, "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC7_invalid_from_iban_too_short(self):
        with self.assertRaises(Exception):
            transfer_request("ES912100041845020005133", VALID_IBAN, "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC8_invalid_from_iban_invalid_length(self):
        with self.assertRaises(Exception):
            transfer_request("ES91210004184502000513321", VALID_IBAN, "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC9_invalid_from_iban_wrong_country(self):
        with self.assertRaises(Exception):
            transfer_request("DE9121000418450200051332", VALID_IBAN, "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC10_invalid_to_iban_numeric(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, "15", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC11_invalid_to_iban_too_short(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, "ES912100041845020005133", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC12_invalid_to_iban_invalid_length(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, "ES91210004184502000513321", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC13_invalid_to_iban_wrong_country(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, "DE9121000418450200051332", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC14_invalid_concept_numeric(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, 15, "ORDINARY", "31/12/2050", 10.0)

    def test_TC15_invalid_concept_random_text(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "random te", "ORDINARY", "31/12/2050", 10.0)

    def test_TC16_invalid_concept_too_long(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text invaliddddddddddddddddddddd", "ORDINARY", "31/12/2050", 10.0)

    def test_TC17_invalid_concept_missing_space(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "textvalid", "ORDINARY", "31/12/2050", 10.0)

    def test_TC18_invalid_concept_special_chars(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text valid**", "ORDINARY", "31/12/2050", 10.0)

    def test_TC19_invalid_type_numeric(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", 15, "31/12/2050", 10.0)

    def test_TC20_invalid_type_unknown(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "RANDOM", "31/12/2050", 10.0)

    def test_TC21_invalid_date_numeric(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", 15, 10.0)

    def test_TC22_invalid_date_month_day_swapped(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "02/31/2026", 10.0)

    def test_TC23_invalid_date_zero_day(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "00/01/2026", 10.0)

    def test_TC24_invalid_date_day_out_of_range(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "32/01/2026", 10.0)

    def test_TC25_invalid_date_zero_month(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/00/2026", 10.0)

    def test_TC26_invalid_date_month_13(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/13/2026", 10.0)

    def test_TC27_invalid_date_past(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2024", 10.0)

    def test_TC28_invalid_date_beyond_2050(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2051", 10.0)

    def test_TC29_invalid_date_format(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "1/2/2026", 10.0)

    def test_TC30_invalid_date_on_edge(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "1/1/2025", 10.0)

    def test_TC31_invalid_amount_non_numeric(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", "text")

    def test_TC32_invalid_amount_too_low(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", 9.99)

    def test_TC33_invalid_amount_too_high(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", 10000.01)

    def test_TC34_invalid_amount_extra_decimal(self):
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", 10.001)

    def test_TC35_duplicate_transfer(self):
        transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", 10.0)
        with self.assertRaises(Exception):
            transfer_request(VALID_IBAN, VALID_IBAN_2, "text validd", "ORDINARY", "01/01/2026", 10.0)