from pva.PvaApi import PvaApi


# for communication with http://smspva.com/ service
class SmsPvaApi(PvaApi):

    def __init__(self, base_url, api_key, service_id, country):
        super().__init__(base_url, api_key, service_id, country)

    def get_balance(self) -> int:
        raise NotImplementedError()

    def get_service_price(self) -> float:
        return 5

    def get_phone_number(self) -> str:
        raise NotImplementedError()

    def get_sms_message(self) -> str:
        raise NotImplementedError()
