import time
from pva.PvaApi import PvaApi


# for communication with http://smspva.com/ service
class SmsPva(PvaApi):

    def __init__(self, base_url, api_key, service_id, country):
        super().__init__(base_url, api_key, service_id, country)
        self.service_price = self.get_service_price()

    def get_balance(self) -> float:
        payload = {'metod': "get_balance",
                   'service': self.service_id, 'apikey': self.api_key}

        response = self.send_request(self.base_url, payload)

        if response["response"] == "1":
            return float(response["balance"])
        else:
            self.handle_error(response)
        return None

    def get_service_price(self) -> float:
        payload = {'metod': "get_service_price",
                   'country': self.country, 'service': self.service_id, 'apikey': self.api_key}

        response = self.send_request(self.base_url, payload)

        if response["response"] == "1":
            return float(response["price"])
        else:
            self.handle_error(response)
        return None

    def request_phone_number(self) -> str:
        payload = {'metod': "get_number",
                   'country': self.country, 'service': self.service_id, 'apikey': self.api_key}

        response = self.send_request(self.base_url, payload)

        if response["response"] == "1":
            self.add_number(response["number"], response["id"])
            return response["number"]
        elif response["response"] == "2":
            print(
                "Number is already taken, will try to request a number again in 60 seconds")
            time.sleep(60)
            return self.request_phone_number()
        else:
            self.handle_error(response)
        return None

    def get_sms_message(self, number: str) -> str:
        stored_number = self.get_stored_number(number)

        payload = {'metod': "get_sms",
                   'country': self.country, 'service': self.service_id, 'id': stored_number.security_id, 'apikey': self.api_key}

        while not stored_number.is_expired():
            response = self.send_request(
                self.base_url + "GetServiceNumber", payload)
            if response["response"] == "1":
                self.del_stored_number(number)
                return self.get_code_from_message(response["sms"])
            elif response["response"] == "2":  # message hasn't been received yet
                time.sleep(20)  # time specified in smspva documentation
                continue
            else:
                self.handle_error(response)
                break

        self.del_stored_number(number)

        return None  # number expires before message was received

    def handle_error(self, response):  # TODO handle all error codes from smspva documentation
        print("error code returned")
        print(response["error_msg"])
