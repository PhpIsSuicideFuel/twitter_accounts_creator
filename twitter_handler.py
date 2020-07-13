import constants.dom_constants as dom_constants
from selenium_helper import SeleniumHelper
from selenium.webdriver.remote.webelement import WebElement
from pva.pva_api import PvaApi
from credential_helper import generate_password, generate_username


class TwitterHandler(SeleniumHelper):

    def __init__(self, driver, pva_api: PvaApi):
        super().__init__(driver)
        self.pva = pva_api

    def create_account(self) -> dict:

        account = {'username': generate_username(),
                   'password': generate_password()}

        self.load_page(dom_constants.DESKTOP_URL_CREATE)
        self.wait_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_NAME,
                            account['username'])

        number = self.submit_phone_details()
        account['number'] = number

        self.wait_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_PASSWORD,
                            account['password'])
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        # code for uploading profile pic goes here
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # code for entering bio goes here
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # "What are you interested in?" page
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # "Suggestions for you to follow" page
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        # "Turn on notifications" page
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SKIP_FOR_NOW)
        # you're in twitter:)

        self.clear_browser_data()  # clearing browser data after account creation
        return account

    def submit_phone_details(self) -> str:
        number = self.pva.request_phone_number()
        if number is None:  # tries until a valid number is returned
            return self.submit_phone_details()

        self.select_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_PHONE,
                              '+' + number)  # write phone number
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_SIGN_UP)
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_OK)

        # if the number expires None will be returned
        code = self.pva.get_sms_message(number)
        if code is None:
            return self.submit_phone_details()

        self.select_and_write(dom_constants.DESKTOP_FIELD_SIGN_UP_CODE,
                              code)  # write verification code
        self.wait_and_click(dom_constants.DESKTOP_BUTTON_NEXT)
        return number

    # loads the clear browser data dialog, selects advanced tab, checks all checkboxes, selects "All time" from dropdown menu and clears the data
    def clear_browser_data(self):
        self.load_page(dom_constants.CLEAR_BROWSER_DATA_URL)
        dialog_box = self.find_shadow_root('settings-ui', "settings-main", "settings-basic-page",
                                           "settings-privacy-page", "settings-clear-browsing-data-dialog")
        tabs = self.get_shadow_element_from(
            dialog_box, "cr-tabs").find_elements_by_tag_name('div')

        advanced_tab_button = self.get_element_by_text("Advanced", tabs)

        if "selected" not in advanced_tab_button.get_attribute("class"):
            # if advanced tab is not selected
            self.click(advanced_tab_button)

        time_range_dropdown = self.create_selector(self.get_shadow_element_from(
            dialog_box, "settings-dropdown-menu").find_element_by_tag_name('select'))
        self.select_by_text("All time", time_range_dropdown)

        settings_checkboxes = dialog_box.find_element_by_css_selector('#advanced-tab').find_elements_by_tag_name(
            'settings-checkbox')

        for checkbox in settings_checkboxes:  # enabling all options
            if checkbox.get_attribute('checked') is None:
                self.click(self.get_shadow_element(
                    checkbox).find_element_by_tag_name('cr-checkbox'))

        self.click(dialog_box.find_element_by_css_selector(
            '#clearBrowsingDataConfirm'))

    def get_element_by_text(self, text: str, elements: list) -> WebElement:
        for element in elements:
            if element.text == text:
                return element

        return None
