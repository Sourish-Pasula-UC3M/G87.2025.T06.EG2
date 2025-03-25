"""Calculates the Balance for a given IBAN"""
import json
import os
from datetime import date
from src.main.python.uc3m_money import AccountManagementException

def validate_iban(iban):
    """
        Validates the format of a Spanish IBAN.
        An IBAN is considered valid if it starts with 'ES', has a total length of 24 characters,
        and the characters after 'ES' are all digits.

        Args:
            iban (str): The IBAN string to validate.
        Returns:
            bool: True if the IBAN is valid, False otherwise.
        """
    if iban.startswith("ES") and len(iban) == 24 and iban[2:].isdigit():
        return True
    return False
def calculate_balance(iban_number):
    """
        This function, validates the provided IBAN, reads transactions and filters them by the given IBAN, sums the
        transaction amounts for that IBAN, creates a balance entry with today's date, and appends the balance
        to 'balances.json'.

        Args:
            iban_number (str): The IBAN number for which the balance is calculated.
        Raises:
            AccountManagementException: If the IBAN is invalid or required files are missing.
        Returns:
            bool: True if the balance was successfully calculated and recorded.
        """

    if not isinstance(iban_number, str):
        raise AccountManagementException("Iban is in invalid format")
    if not validate_iban(iban_number):
        raise AccountManagementException("Iban is not valid")

    def file_path_found():
        path = os.path.join(os.path.dirname(__file__), "..", "..", "transactions.json")

        absolute_path = os.path.abspath(path)
        if os.path.exists(path) is not True:
            raise AccountManagementException(f"Transactions file not found at: {absolute_path}")

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key in data:
            if key["IBAN"] == iban_number:
                return True
        return False

    file_path_found()

    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "transactions.json")
    with open(file_path, "r", encoding="utf-8") as file:
        file_data = json.load(file)

    amount = 0
    for i in file_data:
        if i["IBAN"] == iban_number:
            amount += float(i["amount"])

    balance = {
        "iban": iban_number,
        "amount": amount,
        "date": date.today().isoformat()
    }

    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "balances.json")
    if not os.path.exists(output_path):
        raise AccountManagementException("JSON file does not exist")

    with open(output_path, "r", encoding="utf-8") as file:
        output_data = json.load(file)

    output_data.append(balance)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)  # type: ignore

    return True

