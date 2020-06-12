import requests
from pva.PvaApi import PvaApi


# for communication with https://www.smscodes.io/ service
class SmsCodesApi(PvaApi):

    def __init__(self, base_url, api_key, service_id, country):
        super().__init__(base_url, api_key, service_id, country)
        self.service_price = self.get_service_price()
        self.numbers = dict()

    def get_balance(self) -> float:
        payload = {'key': self.api_key}
        try:
            response = requests.get(self.base_url + "GetBalance",
                                    params=payload).json()
        except:
            print("request exception")
            response = None

        if response["Status"] == "Success":
            return float(response["Balance"])
        else:
            self.handle_error(response)
        return None

    def get_service_price(self) -> float:
        payload = {'iso': self.country,
                   'serviceId': self.service_id, 'key': self.api_key}
        try:
            response = requests.get(
                self.base_url + "GetServiceCountryPrices", params=payload).json()
        except:
            print("request exception")
            response = None

        if response["Status"] == "Success":
            price = response["Prices"][0]  # SmsCodes returns a list of prices
            return float(price["Price"])
        else:
            self.handle_error(response)
        return None

    def get_phone_number(self) -> str:
        payload = {'key': self.api_key,
                   'iso': self.country, 'serv': self.service_id}
        try:
            response = requests.get(
                self.base_url + "GetServiceNumber", params=payload).json()
        except:
            print("request exception")
            response = None

        if response["Status"] == "Success":
            self.numbers[response["Number"]] = response["SecurityId"]
            print(response["SecurityId"])
            return response["Number"]
        else:
            self.handle_error(response)
        return None

    def get_sms_message(self, number: str) -> str:
        payload = {'key': self.api_key,
                   'sid': self.numbers.get(number), 'number': number}
        try:
            response = requests.get(
                self.base_url + "GetServiceNumber", params=payload).json()
        except:
            print("request exception")
            response = None

        if response["Status"] == "Success":
            del self.numbers[number]
            return self.get_code_from_message(response["SMS"])
        else:
            self.handle_error(response)
        return None

    def handle_error(self, response):  # sms codes didn't document their error codes
        print("error code returned")
        print(response)
