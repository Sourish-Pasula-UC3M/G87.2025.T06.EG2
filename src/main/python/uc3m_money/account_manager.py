"""Module """

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        if iban.startswith("ES") and len(iban) == 24 and iban[2:].isdigit():
            return True
        return False
