
class PvaApi:

    def __init__(self, base_url, api_key, service_id, country):
        self.base_url = base_url
        self.api_key = api_key
        self.service_id = service_id
        self.country = country

    def get_balance(self) -> int:
        # returns current balance
        pass

    def get_service_price(self) -> float:
        # returns service price
        pass

    def get_phone_number(self) -> str:
        # returns a new phone number
        pass

    def get_sms_message(self) -> str:
        # fetches the latest message from the current number
        pass

    def get_code_from_message(self, message: str) -> str:
        # extracts the code from message
        pass

    def print(self):
        return f"{self.base_url} | {self.api_key}"
