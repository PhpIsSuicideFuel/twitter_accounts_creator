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

        if self.submit_phone_details():
            self.waitAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_PASSWORD,
                              account['password'])
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_NEXT)
            # code for uploading profile pic goes here
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
            # code for entering bio goes here
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
            # "What are you interested in?" page
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
            # "Suggestions for you to follow" page
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_NEXT)
            # "Turn on notifications" page
            self.waitAndClick(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
            # you're in twitter:)

        return account

    def submit_phone_details(self) -> bool:
        number = self.pva.request_phone_number()
        if number is None:  # tries until a valid number is returned
            return self.submit_phone_details()

        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                            number)  # get phone number
        self.waitAndClick(dom_constants.DESKTOP_BUTTON_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_BUTTON_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_BUTTON_SIGN_UP)
        self.waitAndClick(dom_constants.DESKTOP_BUTTON_OK)

        code = self.pva.get_sms_message(number)
        if code is None:
            return self.submit_phone_details()

        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                            code)  # get verification code
        self.waitAndClick(dom_constants.DESKTOP_BUTTON_NEXT)
        return True
