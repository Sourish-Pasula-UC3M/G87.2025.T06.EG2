import hashlib
import json
import re
from datetime import datetime, timezone
from account_manager import AccountManager

class TransferRequest:
    VALID_TRANSFER_TYPES = {"ORDINARY", "URGENT", "IMMEDIATE"}
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
        self.store_transfer()

    def generate_transfer_code(self):
        """Returns the MD5 signature of the transfer."""
        return hashlib.md5(str(self).encode()).hexdigest()

    def store_transfer(self):
        """Stores the transfer in a JSON file if it doesn't already exist."""
        transfer_data = self.to_json()
        try:
            with open(self.TRANSFER_FILE, "r", encoding="utf-8") as file:
                transfers = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            transfers = []

        if transfer_data in transfers:
            raise ValueError("Duplicate transfer detected.")

        transfers.append(transfer_data)
        with open(self.TRANSFER_FILE, "w", encoding="utf-8") as file:
            json.dump(transfers, file, indent=4)

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
        if not AccountManager.validate_iban(value):
            raise ValueError("Invalid IBAN.")
        self.__from_iban = value

    @property
    def to_iban(self):
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        if not AccountManager.validate_iban(value):
            raise ValueError("Invalid IBAN.")
        self.__to_iban = value

    @property
    def transfer_concept(self):
        return self.__transfer_concept

    @transfer_concept.setter
    def transfer_concept(self, value):
        if not (10 <= len(value) <= 30 and re.search(r"[a-zA-Z]+\s+[a-zA-Z]+", value)):
            raise ValueError("Invalid concept. Must be 10-30 chars with at least two words.")
        self.__transfer_concept = value

    @property
    def transfer_type(self):
        return self.__transfer_type

    @transfer_type.setter
    def transfer_type(self, value):
        if value not in self.VALID_TRANSFER_TYPES:
            raise ValueError(f"Invalid transfer type: {value}.")
        self.__transfer_type = value

    @property
    def transfer_date(self):
        return self.__transfer_date

    @transfer_date.setter
    def transfer_date(self, value):
        try:
            date_obj = datetime.strptime(value, "%d/%m/%Y")
            if date_obj.year < 2025 or date_obj.year >= 2051:
                raise ValueError("Year must be between 2025 and 2050.")
            if date_obj.date() < datetime.now().date():
                raise ValueError("Transfer date must be today or in the future.")
        except ValueError:
            raise ValueError("Invalid date format. Must be DD/MM/YYYY.")
        self.__transfer_date = value

    @property
    def transfer_amount(self):
        return self.__transfer_amount

    @transfer_amount.setter
    def transfer_amount(self, value):
        if not (10.00 <= value <= 10000.00) or len(str(value).split(".")[-1]) > 2:
            raise ValueError("Amount must be between 10.00 and 10000.00 with max 2 decimals.")
        self.__transfer_amount = value

    @property
    def time_stamp(self):
        return self.__time_stamp

    @property
    def transfer_code(self):
        return self.__transfer_code

    def __str__(self):
        return json.dumps(self.to_json())
