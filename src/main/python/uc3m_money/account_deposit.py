"""Contains the class OrderShipping"""
from datetime import datetime, timezone
import json
import os
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager
import hashlib

class AccountDeposit:
    """Class representing the information required for shipping of an order"""

    def __init__(self,
                 to_iban: str,
                 deposit_amount):
        #check to_iban
        if not isinstance(to_iban, str):
            raise AccountManagementException("To_iban must be a string")

        if not AccountManager.validate_iban(to_iban):
            raise AccountManagementException("Invalid to_iban")
        try:
            deposit_amount = float(deposit_amount)
        except ValueError as exc:
            raise AccountManagementException("Invalid amount format") from exc

        if deposit_amount <= 0:
            raise AccountManagementException("Amount must be positive")
        if deposit_amount < 10.00:
            raise AccountManagementException("Amount must be >= 10.00")
        if deposit_amount > 10000.00:
            raise AccountManagementException("Amount must be <= 10000.00")

        if len(str(deposit_amount).split(".")[1]) > 2:
            raise AccountManagementException("Amount must have 2 decimal places")

        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """returns the object data in json format"""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """Property that represents the product_id of the patient"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Property that represents the order_id"""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Property that represents the phone number of the client"""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date( self, value ):
        self.__deposit_date = value


    @property
    def deposit_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

def deposit_into_account(input_file):
    """
        Processes a deposit into an account by reading deposit data from a JSON file.

        The input JSON file must contain a dictionary with keys "IBAN" (string) and "AMOUNT"
        (string in the format "EUR <amount>"). This function validates the IBAN, ensures the
        amount is positive and less than or equal to 10,000 EUR, and then saves the deposit
        information to a shared deposits file (`deposits.json`).

        Args:
            input_file (str): Path to the JSON file containing the deposit data.

        Returns:
            str: A unique deposit signature generated for the successful deposit.

        Raises:
            AccountManagementException: If the file is missing, not in valid JSON format,
            lacks required fields, contains invalid data (e.g., IBAN, currency, amount),
            or if the amount is out of acceptable bounds.
        """
    if not os.path.exists(input_file):
        raise AccountManagementException("Data file is not found.")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise AccountManagementException("The file is not in JSON format.") from exc

    if not isinstance(data, dict) or "AMOUNT" not in data or "IBAN" not in data:
        raise AccountManagementException("The JSON does not have the expected structure.")


    iban = data["IBAN"]
    amount = data["AMOUNT"]

    if not AccountManager.validate_iban(iban):
        raise AccountManagementException("The iban is invalid.")

    if not amount.startswith("EUR "):
        raise AccountManagementException("Currency must be EUR.")

    try:
        amount = float(amount.split("EUR ")[1])
    except ValueError as exc:
        raise AccountManagementException("Amount format invalid") from exc

    if amount > 10000.00:
        raise AccountManagementException("Amount must be <= 10000.00")
    if amount <= 0:
        raise AccountManagementException("Amount must be > 0.")


    deposit = AccountDeposit(iban, amount)

    directory = os.path.dirname(__file__)
    path = os.path.join(directory, "..", "..", "deposits.json")

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                deposits = json.load(f)
                if not isinstance(deposits, list):
                    deposits = []
            except json.JSONDecodeError:
                deposits = []
    else:
        deposits = []
    deposits.append(deposit.to_json())
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(deposits, f, indent=4)  # type: ignore

    return deposit.deposit_signature



