import re


class PvaApi:

    def __init__(self, base_url, api_key, service_id, country):
        self.base_url = base_url
        self.api_key = api_key
        self.service_id = service_id
        self.country = country

    def get_balance(self) -> float:
        # returns current balance
        pass

    def get_service_price(self) -> float:
        # returns service price
        pass

    def get_phone_number(self) -> str:
        # returns a new phone number
        pass

    def get_sms_message(self, number: str) -> str:
        # fetches the latest message from the specified number
        pass

    def handle_error(self, response: dict):
        # handle errors if they occur
        pass

    # extracts the code from message
    def get_code_from_message(self, message: str) -> str:
        try:
            code = re.search(r'(^\d+)', self.code).group(1)
        except AttributeError:
            print(f"failed to extract code from: {code}")
        return code

    def print(self):
        return f"{self.base_url} | {self.api_key}"
