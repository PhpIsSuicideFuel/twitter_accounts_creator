import constants.dom_constants as dom_constants
from SeleniumHelper import SeleniumHelper
from pva.PvaApi import PvaApi
from typing import NewType


class TwitterHandler(SeleniumHelper):

    def __init__(self, driver, pva_api: PvaApi):
        super().__init__(driver)
        self.pva = pva_api

    def create_account(self, name, password, pva):
        self.load_page(dom_constants.DESKTOP_URL_CREATE)
        self.waitAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_NAME,
                          name)
        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                            self.pva.request_phone_number())  # get phone number
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_SIGN_UP)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_OK)
        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                            '12345')  # get verification code
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
