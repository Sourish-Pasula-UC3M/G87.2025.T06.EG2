"""Module """

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """
            Validate the format of a Spanish IBAN.

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
