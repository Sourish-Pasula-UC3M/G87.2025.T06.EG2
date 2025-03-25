"""Calculates the Balance for a given IBAN"""
import json
import os
from datetime import date
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager


def calculate_balance(iban_number):
    """
    Validates the IBAN, sums all transactions for it from 'transactions.json',
    and appends the balance to 'balances.json' (if amount ≠ 0).

    Args:
        iban_number (str): The IBAN number for which the balance is calculated.

    Returns:
        bool: True if the balance was successfully calculated and (if non-zero) recorded.

    Raises:
        AccountManagementException: If the IBAN is invalid or files are missing/corrupt.
    """

    # Validate IBAN
    if not isinstance(iban_number, str):
        raise AccountManagementException("IBAN must be a string")
    if not AccountManager.validate_iban(iban_number):
        raise AccountManagementException("IBAN is not valid")

    # Define file paths
    transactions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "transactions.json"))
    balances_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "balances.json"))

    # Check if transactions.json exists
    if not os.path.exists(transactions_path):
        raise AccountManagementException("Transactions file not found")

    # Load transactions
    try:
        with open(transactions_path, "r", encoding="utf-8") as file:
            transactions_data = json.load(file)
            if not isinstance(transactions_data, list):
                raise AccountManagementException("Transactions file format is invalid")
    except json.JSONDecodeError:
        raise AccountManagementException("Transactions file is empty or corrupted")

    # Filter and sum amounts
    amount = 0.0
    found = False
    for transaction in transactions_data:
        print(transaction)
        if transaction.get("IBAN") == iban_number:
            found = True
            try:
                amount += float(transaction.get("amount"))
            except ValueError:
                raise AccountManagementException("Amount format in transactions file is invalid")
    if not found:
        raise AccountManagementException("No transactions for this IBAN")

    # Return True but don't write if no transactions were found

    if amount == 0.0:
        return True

    # Prepare balance entry
    balance_entry = {
        "iban": iban_number,
        "amount": amount,
        "date": date.today().isoformat()
    }

    # Check if balances.json exists
    if not os.path.exists(balances_path):
        raise AccountManagementException("Balances file not found")

    # Load balances data
    try:
        with open(balances_path, "r", encoding="utf-8") as f:
            balances_data = json.load(f)
            if not isinstance(balances_data, list):
                raise AccountManagementException("Balances file format is invalid")
    except json.JSONDecodeError:
        raise AccountManagementException("Balances file is empty or corrupted")

    # Append new balance and save
    balances_data.append(balance_entry)
    with open(balances_path, "w", encoding="utf-8") as f:
        json.dump(balances_data, f, indent=4)

    return True
