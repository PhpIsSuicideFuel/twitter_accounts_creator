from SeleniumHelper import SeleniumHelper
import constants.dom_constants as dom_constants


class TwitterHandler(SeleniumHelper):

    def create_account(self, name, password, pva):
        self.load_page(dom_constants.DESKTOP_URL_CREATE)
        self.waitAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_NAME,
                          name)
        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                            '865661441') # get phone number
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_SIGN_UP)
        self.waitAndClick(dom_constants.DESKTOP_FIELD_OK)
        self.selectAndWrite(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                            pva.phoneVerification()) # get verification code
        self.waitAndClick(dom_constants.DESKTOP_FIELD_NEXT)
