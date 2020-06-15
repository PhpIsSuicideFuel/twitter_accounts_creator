import constants.dom_constants as dom_constants
from SeleniumHelper import SeleniumHelper
from pva.PvaApi import PvaApi
from CredentialHelper import generate_password, generate_username


class TwitterHandler(SeleniumHelper):

    def __init__(self, driver, pva_api: PvaApi):
        super().__init__(driver)
        self.pva = pva_api

    def create_account(self) -> dict:
        self.clear_browser_data()

        # account = {'username': generate_username(),
        #            'password': generate_password()}

        # self.load_page(dom_constants.DESKTOP_URL_CREATE)
        # self.wait_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_NAME,
        #                     account['username'])

        # number = self.submit_phone_details()
        # account['number'] = number

        # self.wait_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_PASSWORD,
        #                     account['password'])
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        # # code for uploading profile pic goes here
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # # code for entering bio goes here
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # # "What are you interested in?" page
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # # "Suggestions for you to follow" page
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        # # "Turn on notifications" page
        # self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # # you're in twitter:)

        # return account

    def submit_phone_details(self) -> str:
        number = self.pva.request_phone_number()
        if number is None:  # tries until a valid number is returned
            return self.submit_phone_details()

        self.select_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                              '+' + number)  # get phone number
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SIGN_UP)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_OK)

        code = self.pva.get_sms_message(number)
        if code is None:
            return self.submit_phone_details()

        self.select_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                              code)  # get verification code
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        return number

    def clear_browser_data(self):
        self.load_page(dom_constants.CLEAR_BROWSER_DATA_URL)
        advanced_button = self.wait_show_element(
            dom_constants.DESKTOP_BUTTON_ADVANCED)
        print(advanced_button)
        attr = self.get_element_attribute(
            advanced_button, "aria-selected")
        print(attr)
        if attr == "false":
            self.click(advanced_button)
