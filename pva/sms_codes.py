import time
from pva.pva_api import PvaApi


# for communication with https://www.smscodes.io/ service
class SmsCodes(PvaApi):

    def __init__(self, base_url, api_key, service_id, country):
        super().__init__(base_url, api_key, service_id, country)
        self.service_price = self.get_service_price()
        self.get_balance()

    def get_balance(self) -> float:
        payload = {'key': self.api_key}

        response = self.send_request(self.base_url + "GetBalance", payload)

        if response["Status"] == "Success":
            self.balance = float(response["Balance"]) / 100
            return float(response["Balance"]) / 100
        else:
            self.handle_error(response)
        return None

    def get_service_price(self) -> float:
        payload = {'iso': self.country,
                   'serviceId': self.service_id, 'key': self.api_key}

        response = self.send_request(
            self.base_url + "GetServiceCountryPrices", payload)

        if response["Status"] == "Success":
            price = response["Prices"][0]  # SmsCodes returns a list of prices
            return float(price["Price"])
        else:
            self.handle_error(response)
        return None

    def request_phone_number(self) -> str:
        payload = {'key': self.api_key,
                   'iso': self.country, 'serv': self.service_id}

        response = self.send_request(
            self.base_url + "GetServiceNumber", payload)

        if response["Status"] == "Success":
            self.add_number(response["Number"], response["SecurityId"])
            return response["Number"]
        else:
            self.handle_error(response)
        return None

    # attempts to fetch the code from provided number, returns None only if the number expires or an error occurs
    def get_sms_message(self, number: str) -> str:
        stored_number = self.get_stored_number(number)

        payload = {'key': self.api_key,
                   'sid': stored_number.security_id, 'number': number}

        while not stored_number.is_expired():
            response = self.send_request(
                self.base_url + "GetSMSCode", payload)
            if response["Status"] == "Success":
                if response["SMS"] == "Message not received yet":
                    continue
                else:
                    self.del_stored_number(number)
                    return self.get_code_from_message(response["SMS"])
            else:
                self.handle_error(response)
                break

        self.del_stored_number(number)

        return None  # number expires before message was received

    def handle_error(self, response):  # smscodes.io didn't document their error codes
        print("error code returned")
        print(response)
