from pva.PvaApi import PvaApi


# for communication with http://smspva.com/ service
class SmsPvaApi(PvaApi):

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
        raise NotImplementedError()

    def get_sms_message(self, number: str) -> str:
        raise NotImplementedError()

    def handle_error(self, response):  # TODO handle all error codes from smspva documentation
        print("error code returned")
        print(response["error_msg"])
