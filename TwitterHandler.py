import constants.dom_constants as dom_constants
from SeleniumHelper import SeleniumHelper
from pva.PvaApi import PvaApi
from CredentialHelper import generate_password, generate_username


class TwitterHandler(SeleniumHelper):

    def __init__(self, driver, pva_api: PvaApi):
        super().__init__(driver)
        self.pva = pva_api

    def create_account(self) -> dict:
        account = {'username': generate_username(),
                   'password': generate_password()}

        self.load_page(dom_constants.DESKTOP_URL_CREATE)
        self.waitAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_NAME,
                          account['username'])

        self.submit_phone_details()

        return account

    def submit_phone_details(self) -> bool:
        number = self.pva.request_phone_number()

        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                            number)  # get phone number
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_SIGN_UP)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_OK)

        code = self.pva.get_sms_message(number)
        if code is None:
            # need to request and use different number here
            return None

        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                            code)  # get verification code
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
