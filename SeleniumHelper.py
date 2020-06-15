from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumHelper:

    WAIT = 99999

    def __init__(self, web_driver: WebDriver):
        self.driver = web_driver

    def load_page(self, page):
        try:
            self.driver.get(page)
            return True
        except:
            return False

    def submit_form(self, element):
        try:
            element.submit()
            return True
        except TimeoutException:
            return False

    def submit_form_selector(self, selector):
        try:
            element = self.getElement(selector)
            element.submit()
            return True
        except TimeoutException:
            return False

    def wait_show_element(self, selector, wait=99999):
        try:
            wait = WebDriverWait(self.driver, wait)
            element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, selector)))
            return element
        except:
            return None

    def waitHideElement(self, selector, wait):
        try:
            wait = WebDriverWait(self.driver, wait)
            element = wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, selector)))
            return element
        except:
            return None

    def getElementFrom(self, fromObject, selector):
        try:
            return fromObject.find_element_by_xpath(selector)
        except NoSuchElementException:
            return None

    def getElementsFrom(self, fromObject, selector):
        try:
            return fromObject.find_elements_by_xpath(selector)
        except NoSuchElementException:
            return None

    def getElement(self, selector):
        return self.getElementFrom(self.driver, selector)

    def getElements(self, selector):
        return self.getElementsFrom(self.driver, selector)

    def getElementFromValue(self, fromObject, selector):
        element = self.getElementFrom(fromObject, selector)
        if element:
            return element.text
        return None

    def getElementValue(self, selector):
        element = self.getElement(selector)
        if element:
            return element.text
        return None

    def getElementFromAttribute(self, fromObject, selector, attribute):
        element = self.getElementFrom(fromObject, selector)
        if element:
            return element.get_attribute(attribute)
        return None

    def get_element_attribute(self, element, attribute):
        if element:
            return element.get_attribute(attribute)
        return None

    def get_parent_node(self, node):
        return node.find_element_by_xpath('..')

    def get_child_nodes(self, node):
        return node.find_elements_by_xpath('./*')

    def select_and_write(self, field, value):
        fieldObject = self.getElement(field)
        fieldObject.send_keys(value)
        return fieldObject

    def wait_and_write(self, field, value):
        fieldObject = self.wait_show_element(field, self.WAIT)
        fieldObject.send_keys(value)
        return fieldObject

    def wait_and_click(self, field):
        fieldObject = self.wait_show_element(field, self.WAIT)
        self.click(fieldObject)
        return fieldObject

    def click_selector(self, selector):
        element = self.getElement(selector)
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def click(self, element):
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def move_to_element(self, element):
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", element)
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.perform()

    def save_screenshot(self, path="screenshot.png"):
        self.driver.save_screenshot(path)

    def get_between(self, text, strInit, strEnd):
        exit = None
        arr1 = text.split(strInit)
        if len(arr1) > 1:
            arr2 = arr1[1].split(strEnd)
            exit = arr2[0]
        return exit

    def get_chars_from(self, text, strInit, count):
        exit = None
        arr1 = text.split(strInit)
        if len(arr1) > 1:
            substr = arr1[1]
            exit = substr[:count]
        return exit

    def close(self):
        self.driver.close()
