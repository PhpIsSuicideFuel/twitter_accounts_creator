import re
import requests
from datetime import datetime


class PhoneNumber:

    def __init__(self, number, security_id):
        self.number = number
        self.security_id = security_id
        self.creation_time = datetime.now()


class PvaApi:

    def __init__(self, base_url, api_key, service_id, country):
        self.base_url = base_url
        self.api_key = api_key
        self.service_id = service_id
        self.country = country
        self.numbers = []

    def get_balance(self) -> float:
        # returns current balance
        raise NotImplementedError

    def get_service_price(self) -> float:
        # returns service price
        raise NotImplementedError

    def request_phone_number(self) -> str:
        # returns a new phone number
        raise NotImplementedError

    def get_sms_message(self, number: str) -> str:
        # fetches the latest message from the specified number
        raise NotImplementedError

    def handle_error(self, response: dict):
        # handle errors if they occur
        raise NotImplementedError

    def send_request(self, url: str, payload: dict) -> dict:
        try:
            response = requests.get(url,
                                    params=payload).json()
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return response

    def add_number(self, number: str, security_id: str):
        self.numbers.append(PhoneNumber(number, security_id))

    # returns a PhoneNumber object that matches the provided phone number
    def get_stored_number(self, number: str) -> PhoneNumber:
        return next((num for num in self.numbers if num.number == number), None)

    # extracts the code from message
    def get_code_from_message(self, message: str) -> str:
        try:
            code = re.search(r'(^\d+)', message).group(1)
        except AttributeError:
            print(f"failed to extract code from: {message}")
        return code

    def print(self):
        return f"{self.base_url} | {self.api_key}"
