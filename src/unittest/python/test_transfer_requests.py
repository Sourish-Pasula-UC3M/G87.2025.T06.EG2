import unittest
import re
from uc3m_money.transfer_request import transfer_request

VALID_IBAN = "ES9121000418450200051332"
VALID_IBAN_2 = "ES9820385778983000760236"
def is_valid_md5(s):
    return isinstance(s, str) and re.fullmatch(r'[a-fA-F0-9]{32}', s) is not None

class TestTransferRequest(unittest.TestCase):

    def test_TC1_valid_transfer(self):
        result = transfer_request("ES9121000418450200051001", "ES9121000418450200051002", "text valid", "ORDINARY", "01/01/2026", 10.00)
        self.assertTrue(is_valid_md5(result))

    def test_TC2_valid_urgent_transfer(self):
        result = transfer_request("ES9121000418450200051003", "ES9121000418450200051004", "text is valid", "URGENT", "02/02/2049", 10.01)
        self.assertTrue(is_valid_md5(result))

    def test_TC3_valid_immediate_high_amount(self):
        result = transfer_request("ES9121000418450200051005", "ES9121000418450200051006", "text validdddddddddddddddddd", "IMMEDIATE", "30/11/2025", 9999.99)
        self.assertTrue(is_valid_md5(result))

    def test_TC4_valid_ordinary_max_amount(self):
        result = transfer_request("ES9121000418450200051007", "ES9121000418450200051008", "text validddddddddddddddddddd", "ORDINARY", "31/12/2050", 10000.00)
        self.assertTrue(is_valid_md5(result))

    def test_TC5_valid_small_transfer(self):
        result = transfer_request("ES9121000418450200051009", "ES9121000418450200051010", "text validddddddddddddddddddd", "ORDINARY", "31/12/2050", 15.20)
        self.assertTrue(is_valid_md5(result))

    def test_TC6_invalid_from_iban_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("15", "ES9121000418450200051011", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC7_invalid_from_iban_too_short(self):
        with self.assertRaises(Exception):
            transfer_request("ES912100041845020005133", "ES9121000418450200051012", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC8_invalid_from_iban_invalid_length(self):
        with self.assertRaises(Exception):
            transfer_request("ES91210004184502000513321", "ES9121000418450200051013", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC9_invalid_from_iban_wrong_country(self):
        with self.assertRaises(Exception):
            transfer_request("DE9121000418450200051332", "ES9121000418450200051014", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC10_invalid_to_iban_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051015", "15", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC11_invalid_to_iban_too_short(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051016", "ES912100041845020005133", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC12_invalid_to_iban_invalid_length(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051017", "ES91210004184502000513321", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC13_invalid_to_iban_wrong_country(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051018", "DE9121000418450200051332", "text valid test", "ORDINARY", "31/12/2050", 15.2)

    def test_TC14_invalid_concept_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051019", "ES9121000418450200051020", 15, "ORDINARY", "31/12/2050", 10.0)

    def test_TC15_invalid_concept_random_text(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051021", "ES9121000418450200051022", "random te", "ORDINARY", "31/12/2050", 10.0)

    def test_TC16_invalid_concept_too_long(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051023", "ES9121000418450200051024", "text invaliddddddddddddddddddddd", "ORDINARY", "31/12/2050", 10.0)

    def test_TC17_invalid_concept_missing_space(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051025", "ES9121000418450200051026", "textvalid", "ORDINARY", "31/12/2050", 10.0)

    def test_TC18_invalid_concept_special_chars(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051027", "ES9121000418450200051028", "text valid**", "ORDINARY", "31/12/2050", 10.0)

    def test_TC19_invalid_type_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051029", "ES9121000418450200051030", "text validd", 15, "31/12/2050", 10.0)

    def test_TC20_invalid_type_unknown(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051031", "ES9121000418450200051032", "text validd", "RANDOM", "31/12/2050", 10.0)

    def test_TC21_invalid_date_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051033", "ES9121000418450200051034", "text validd", "ORDINARY", 15, 10.0)

    def test_TC22_invalid_date_month_day_swapped(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051035", "ES9121000418450200051036", "text validd", "ORDINARY", "02/31/2026", 10.0)

    def test_TC23_invalid_date_zero_day(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051037", "ES9121000418450200051038", "text validd", "ORDINARY", "00/01/2026", 10.0)

    def test_TC24_invalid_date_day_out_of_range(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051039", "ES9121000418450200051040", "text validd", "ORDINARY", "32/01/2026", 10.0)

    def test_TC25_invalid_date_zero_month(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051041", "ES9121000418450200051042", "text validd", "ORDINARY", "01/00/2026", 10.0)

    def test_TC26_invalid_date_month_13(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051043", "ES9121000418450200051044", "text validd", "ORDINARY", "01/13/2026", 10.0)

    def test_TC27_invalid_date_past(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051045", "ES9121000418450200051046", "text validd", "ORDINARY", "01/01/2024", 10.0)

    def test_TC28_invalid_date_beyond_2050(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051047", "ES9121000418450200051048", "text validd", "ORDINARY", "01/01/2051", 10.0)

    def test_TC29_invalid_date_format(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051049", "ES9121000418450200051050", "text validd", "ORDINARY", "1/2/2026", 10.0)

    def test_TC30_invalid_date_on_edge(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051051", "ES9121000418450200051052", "text validd", "ORDINARY", "1/1/2025", 10.0)

    def test_TC31_invalid_amount_non_numeric(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051053", "ES9121000418450200051054", "text validd", "ORDINARY", "01/01/2026", "text")

    def test_TC32_invalid_amount_too_low(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051055", "ES9121000418450200051056", "text validd", "ORDINARY", "01/01/2026", 9.99)

    def test_TC33_invalid_amount_too_high(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051057", "ES9121000418450200051058", "text validd", "ORDINARY", "01/01/2026", 10000.01)

    def test_TC34_invalid_amount_extra_decimal(self):
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051059", "ES9121000418450200051060", "text validd", "ORDINARY", "01/01/2026", 10.001)

    def test_TC35_duplicate_transfer(self):
        transfer_request("ES9121000418450200051061", "ES9121000418450200051062", "text validd", "ORDINARY", "01/01/2026", 10.0)
        with self.assertRaises(Exception):
            transfer_request("ES9121000418450200051061", "ES9121000418450200051062", "text validd", "ORDINARY", "01/01/2026", 10.0)
