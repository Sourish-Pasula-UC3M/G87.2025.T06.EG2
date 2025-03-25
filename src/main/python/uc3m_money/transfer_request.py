import hashlib
import json
import re
import os
from datetime import datetime, timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.account_manager import AccountManager


class TransferRequest:
    TRANSFER_FILE = "past_transactions.json"

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
        transfer_data = f"{self.from_iban}{self.to_iban}{self.transfer_concept}" \
                        f"{self.transfer_type}{self.transfer_date}{self.transfer_amount}"
        return hashlib.md5(transfer_data.encode()).hexdigest()

    def to_json(self):
        return {
            "from_iban": self.from_iban,
            "to_iban": self.to_iban,
            "transfer_concept": self.transfer_concept,
            "transfer_type": self.transfer_type,
            "transfer_date": self.transfer_date,
            "transfer_amount": self.transfer_amount,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.__transfer_code
        }

    @property
    def transfer_code(self):
        return self.__transfer_code

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)


def transfer_request(from_iban, to_iban, concept, transfer_type, date, amount):
    """
    Processes a transfer request by validating input fields and storing the transaction if it is not a duplicate.
    """
    if not isinstance(from_iban, str):
        raise AccountManagementException("from_iban must be a string")
    if not AccountManager.validate_iban(from_iban):
        raise AccountManagementException("From IBAN is not valid")

    if not isinstance(to_iban, str):
        raise AccountManagementException("to_iban must be a string")
    if not AccountManager.validate_iban(to_iban):
        raise AccountManagementException("To IBAN is not valid")

    # Validate concept
    if not isinstance(concept, str):
        raise AccountManagementException("Concept must be a string")

    # Must be 10-30 characters and contain at least two words
    if not (10 <= len(concept) <= 30 and re.search(r"\b\w+\b.*\b\w+\b", concept)):
        raise AccountManagementException("Invalid concept. Must be 10-30 chars with at least two words.")

    # Must not contain special characters
    if not re.fullmatch(r"[a-zA-Z0-9 ]+", concept):
        raise AccountManagementException("Concept must not contain special characters.")

    if not isinstance(transfer_type, str):
        raise AccountManagementException("transfer_type must be a string")
    valid_types = {"ORDINARY", "URGENT", "IMMEDIATE"}
    if transfer_type not in valid_types:
        raise AccountManagementException(f"Invalid transfer type: {transfer_type}.")

    if not isinstance(date, str):
        raise AccountManagementException("Date must be a string")

    # Check date format explicitly using regex (must be DD/MM/YYYY with two digits for DD and MM)
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", date):
        raise AccountManagementException("Invalid date format. Must be DD/MM/YYYY with two-digit day and month.")

    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        if not (2025 <= date_obj.year <= 2050):
            raise AccountManagementException("Year must be between 2025 and 2050.")
        if date_obj.date() < datetime.now().date():
            raise AccountManagementException("Transfer date must be today or in the future.")
    except ValueError as exc:
        raise AccountManagementException("Invalid date. Must be a valid calendar date.") from exc

    if not isinstance(amount, float):
        raise AccountManagementException("Amount must be a float")
    if len(str(amount).split('.')[-1]) > 2:
        raise AccountManagementException("Amount must have up to two decimal places.")
    if not 10.00 <= amount <= 10000.00:
        raise AccountManagementException("Amount is not within the allowed range (10.00 to 10000.00).")

    transfer_req = TransferRequest(from_iban, to_iban, concept, transfer_type, date, amount)

    directory = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(directory, TransferRequest.TRANSFER_FILE)

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
        if t.get("transfer_code") == transfer_req.transfer_code:
            raise AccountManagementException("Transfer already exists")

    transactions.append(transfer_req.to_json())
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=4)

    return transfer_req.transfer_code
