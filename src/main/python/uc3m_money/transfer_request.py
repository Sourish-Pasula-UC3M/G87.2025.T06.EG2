import hashlib
import json
import re
import os
from datetime import datetime, timezone
import account_management_exception
from src.main.python.uc3m_money.account_manager.py import AccountManager
# pylint: disable=import_error

class TransferRequest:
    TRANSFER_FILE = "transfers.json"

    def __init__(self, from_iban: str, to_iban: str, transfer_concept: str,
                 transfer_type: str, transfer_date: str, transfer_amount: float):
        self.from_iban = from_iban
        self.to_iban = to_iban
        self.transfer_concept = transfer_concept
        self.transfer_type = transfer_type
        self.transfer_date = transfer_date
        self.transfer_amount = transfer_amount
        self.__time_stamp = datetime.timestamp(datetime.now(timezone.utc))
        self.__transfer_code = self.generate_transfer_code()

    def generate_transfer_code(self):
        """Returns the MD5 signature of the transfer."""
        return hashlib.md5(str(self).encode()).hexdigest()

    def to_json(self):
        return {
            "from_iban": self.__from_iban,
            "to_iban": self.__to_iban,
            "transfer_concept": self.__transfer_concept,
            "transfer_type": self.__transfer_type,
            "transfer_date": self.__transfer_date,
            "transfer_amount": self.__transfer_amount,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.__transfer_code
        }

    @property
    def from_iban(self):
        return self.__from_iban

    @from_iban.setter
    def from_iban(self, value):
        self.__from_iban = value

    @property
    def to_iban(self):
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def transfer_concept(self):
        return self.__transfer_concept

    @transfer_concept.setter
    def transfer_concept(self, value):
        self.__transfer_concept = value

    @property
    def transfer_type(self):
        return self.__transfer_type

    @transfer_type.setter
    def transfer_type(self, value):
        self.__transfer_type = value

    @property
    def transfer_date(self):
        return self.__transfer_date

    @transfer_date.setter
    def transfer_date(self, value):
        self.__transfer_date = value

    @property
    def transfer_amount(self):
        return self.__transfer_amount

    @transfer_amount.setter
    def transfer_amount(self, value):
        self.__transfer_amount = value

    @property
    def time_stamp(self):
        return self.__time_stamp

    @property
    def transfer_code(self):
        return self.__transfer_code

    def __str__(self):
        return json.dumps(self.to_json())


def transfer_request(from_iban, to_iban, concept, transfer_type, date, amount):
    """
        Processes a transfer request by validating input fields and storing the transaction if it is not a duplicate.

        This function validates the IBANs, concept string, transfer type, transfer date, and amount.
        If all validations pass and the request does not already exist (based on a unique transfer code),
        it creates an instance of the `TransferRequest` class and saves it to a JSON file.

        Args:
            from_iban (str): Sender's IBAN. Must be a valid IBAN string.
            to_iban (str): Recipient's IBAN. Must be a valid IBAN string.
            concept (str): Description of the transfer. Must be 10–30 characters and contain at least two words.
            transfer_type (str): Type of transfer. Must be one of "ORDINARY", "URGENT", or "IMMEDIATE".
            date (str): Transfer date in "DD/MM/YYYY" format. Must be today or a future date between 2025 and 2050.
            amount (float): Transfer amount. Must be between 10.00 and 10,000.00 inclusive, with up to two decimal places.

        Returns:
            str: A string containing the unique transfer code for the new transaction.

        Raises:
            AccountManagementException: If any input is invalid, improperly formatted, or if the transfer is a duplicate.
        """

    #Check from_iban
    if not isinstance(from_iban, str):
        raise account_management_exception.AccountManagementException("From_iban must be a string")
    if not AccountManager.validate_iban(from_iban):
        raise AccountManagementException("From IBAN is not valid")
    #Check to_iban
    if not isinstance(to_iban, str):
        raise AccountManagementException("To_iban must be a string")
    if not AccountManager.validate_iban(to_iban):
        raise AccountManagementException("To IBAN is not valid")
    #check_concept
    if not isinstance(concept, str):
        raise AccountManagementException("Concept must be a string")
    if not (10 <= len(concept) <= 30 and re.search(r"[a-zA-Z]+\s+[a-zA-Z]+", concept)):
        raise AccountManagementException("Invalid concept. Must be 10-30 chars with at least two words.")

    #check transfer_type
    if not isinstance(transfer_type, str):
        raise AccountManagementException("Transfer_type must be a string")
    valid_types = {"ORDINARY", "URGENT", "IMMEDIATE"}
    if transfer_type not in valid_types:
        raise AccountManagementException(f"Invalid transfer type: {transfer_type}.")

    #check date
    if not isinstance(date,str):
        raise AccountManagementException("Date must be a string")
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        if date_obj.year < 2025 or date_obj.year >= 2051:
            raise AccountManagementException("Year must be between 2025 and 2050.")
        if date_obj.date() < datetime.now().date():
            raise AccountManagementException("Transfer date must be today or in the future.")
    except ValueError as exc:
        raise AccountManagementException("Invalid date format. Must be DD/MM/YYYY.") from exc

    #check amount
    if not isinstance(amount, float):
        raise AccountManagementException("Amount must be a float")
    if len(str(amount).rsplit('.', maxsplit=1)[-1]) > 2:
        raise AccountManagementException("Amount must be between 10.00 and 10000.00 with max 2 decimals.")
    if not 10.00 <= float(amount) <= 10000.00:
        raise AccountManagementException("Amount is not within range")


    #Create an instance of the TransferRequest class
    transfer_req = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)

    directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(directory, "transactions.json")

    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                transactions = json.load(f)
                if not isinstance(transactions, list):
                    transactions = []
            except json.JSONDecodeError:
                transactions = []
    else:
        transactions = []

    for t in transactions:
        if t["transfer_code"] == transfer_req.transfer_code:
            raise AccountManagementException("Transfer already exists")

    with open(path, 'w', encoding='utf-8') as f:
        json.dumps(transactions + [transfer_req.to_json()], f, indent=4) # type: ignore

    return f"Transfer Code: {transfer_req.transfer_code}"