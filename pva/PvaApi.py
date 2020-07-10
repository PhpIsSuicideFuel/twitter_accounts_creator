from abc import ABC, abstractmethod
import re
import requests
import time


class PhoneNumber:
    # time in seconds
    expiry_time = 580

    def __init__(self, number, security_id):
        self.number = number
        self.security_id = security_id
        self.creation_time = time.time()

    def is_expired(self):
        return True if time.time() - self.creation_time >= PhoneNumber.expiry_time else False


class PvaApi(ABC):

    def __init__(self, base_url, api_key, service_id, country, max_requests_minute=30):
        self.base_url = base_url
        self.api_key = api_key
        self.service_id = service_id
        self.country = country
        self.max_requests_minute = max_requests_minute
        self.last_request_time = 0
        self.numbers = []

    @abstractmethod
    def get_balance(self) -> float:
        # returns current balance
        raise NotImplementedError

    @abstractmethod
    def get_service_price(self) -> float:
        # returns service price
        raise NotImplementedError

    @abstractmethod
    def request_phone_number(self) -> str:
        # returns a new phone number
        raise NotImplementedError

    @abstractmethod
    def get_sms_message(self, number: str) -> str:
        # attempts to fetch the code from provided number, returns None only if the number expires or an error occurs
        raise NotImplementedError

    @abstractmethod
    def handle_error(self, response: dict):
        # handle errors if they occur
        raise NotImplementedError

    # uses regex to extract code from a string
    @staticmethod
    def get_code_from_message(message: str) -> str:
        try:
            code = re.search(r'(^\d+)', message).group(1)
        except AttributeError:
            print(f"failed to extract code from: {message}")
        return code

    # sends a http get request to the provided url and with specified parameters, returns a response dictionary
    def send_request(self, url: str, payload: dict) -> dict:
        if time.time() - self.last_request_time > 60 / self.max_requests_minute:
            self.last_request_time = time.time()
            try:
                response = requests.get(url,
                                        params=payload).json()
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
        else:
            print("sleeping for: ", (60 / self.max_requests_minute) -
                  (time.time() - self.last_request_time))
            time.sleep((60 / self.max_requests_minute) -
                       (time.time() - self.last_request_time))  # ensures that you're not exceeding the max_requests_minute so you won't get timed out
            return self.send_request(url, payload)
        return response

    # adds a new PhoneNumber object to the number list
    def add_number(self, number: str, security_id: str):
        self.numbers.append(PhoneNumber(number, security_id))

    # returns a PhoneNumber object that matches the provided phone number
    def get_stored_number(self, number: str) -> PhoneNumber:
        return next((num for num in self.numbers if num.number == number), None)

    # deletes a PhoneNumber from numbers list by matching the number returns True or False if deleted or not
    def del_stored_number(self, number: str) -> bool:
        try:
            self.numbers.remove(self.get_stored_number(number))
            return True
        except ValueError:
            return False

    def print(self):
        return f"{self.base_url} | {self.api_key}"
