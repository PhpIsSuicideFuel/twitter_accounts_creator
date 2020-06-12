import requests
from pva.PvaApi import PvaApi


# for communication with https://www.smscodes.io/ service
class SmsCodesApi(PvaApi):

    def __init__(self, base_url, api_key, service_id, country):
        super().__init__(base_url, api_key, service_id, country)

    def get_balance(self) -> int:
        payload = {'key': self.api_key}
        try:
            r = requests.get(self.base_url + 'GetBalance',
                             params=payload).json()
        except:
            r = None
        if r is not None and r['Status'] == 'Success':
            return int(r['Balance'])
        return None

    def get_service_price(self) -> float:
        return 10

    def get_phone_number(self) -> str:
        raise NotImplementedError()

    def get_sms_message(self) -> str:
        raise NotImplementedError()
