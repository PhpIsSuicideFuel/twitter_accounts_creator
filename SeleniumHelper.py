from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import sys


class SeleniumHelper:

    WAIT = 99999

    def __init__(self, web_driver: WebDriver):
        self.driver = web_driver

    def load_page(self, page) -> bool:
        try:
            self.driver.get(page)
            return True
        except:
            return False

    def submit_form(self, element: WebElement) -> bool:
        try:
            element.submit()
            return True
        except TimeoutException:
            return False

    def submit_form_selector(self, selector: str) -> bool:
        try:
            element = self.get_element(selector)
            element.submit()
            return True
        except TimeoutException:
            return False

    def wait_show_element(self, selector: str, wait=99999) -> WebElement:
        try:
            wait = WebDriverWait(self.driver, wait)
            element = wait.until(EC.visibility_of_element_located(
                (By.XPATH, selector)))
            return element
        except:
            return None

    def wait_show_shadow_element(self, tag_name: str, wait=99999) -> WebElement:
        shadow_parent = self.wait_show_element("//" + tag_name)
        shadow_root = self.driver.execute_script(
            "return arguments[0].shadowRoot", shadow_parent)
        return shadow_root

    def get_shadow_element(self, from_object: WebElement) -> WebElement:
        return self.driver.execute_script("return arguments[0].shadowRoot", from_object)

    def get_shadow_element_from(self, from_object: WebElement, selector: str) -> WebElement:
        try:
            shadow_parent = from_object.find_element_by_tag_name(
                selector)
        except NoSuchElementException:
            print("NoSuchElementException")
        except:
            print("Unexpected error:", sys.exc_info()[0])

        shadow_root = self.driver.execute_script(
            "return arguments[0].shadowRoot", shadow_parent)

        return shadow_root

    def find_shadow_root(self, first_parent: str, *other_parents) -> WebElement:
        current_root = self.wait_show_shadow_element(first_parent)

        for parent_node in other_parents:
            current_root = self.get_shadow_element_from(
                current_root, parent_node)

        return current_root

    def wait_hide_element(self, selector: str, wait) -> WebElement:
        try:
            wait = WebDriverWait(self.driver, wait)
            element = wait.until(EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, selector)))
            return element
        except:
            return None

    def get_element_from(self, from_object, selector: str) -> WebElement:
        try:
            return from_object.find_element_by_xpath(selector)
        except NoSuchElementException:
            return None

    def get_elements_from(self, from_object, selector: str) -> WebElement:
        try:
            return from_object.find_elements_by_xpath(selector)
        except NoSuchElementException:
            return None

    def get_element(self, selector: str) -> WebElement:
        return self.get_element_from(self.driver, selector)

    def get_elements(self, selector: str) -> list:
        return self.get_elements_from(self.driver, selector)

    def get_element_from_value(self, fromObject: WebElement, selector: str) -> str:
        element = self.get_element_from(fromObject, selector)
        if element:
            return element.text
        return None

    def get_element_value(self, selector: str) -> str:
        element = self.get_element(selector)
        if element:
            return element.text
        return None

    def get_element_from_attribute(self, fromObject: WebElement, selector: str, attribute: str):
        element = self.get_element_from(fromObject, selector)
        if element:
            return element.get_attribute(attribute)
        return None

    def get_element_attribute(self, element: WebElement, attribute: str):
        if element:
            return element.get_attribute(attribute)
        return None

    def get_parent_node(self, node: WebElement) -> WebElement:
        return node.find_element_by_xpath('..')

    def get_child_nodes(self, node: WebElement) -> list:
        return node.find_elements_by_xpath('./*')

    def select_and_write(self, field: str, value: str) -> WebElement:
        fieldObject = self.get_element(field)
        fieldObject.send_keys(value)
        return fieldObject

    def wait_and_write(self, selector: str, value: str) -> WebElement:
        fieldObject = self.wait_show_element(selector, self.WAIT)
        fieldObject.send_keys(value)
        return fieldObject

    def wait_and_click(self, selector: str) -> WebElement:
        fieldObject = self.wait_show_element(selector, self.WAIT)
        self.click(fieldObject)
        return fieldObject

    def click_selector(self, selector: str):
        element = self.get_element(selector)
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def click(self, element: WebElement):
        actions = webdriver.ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def move_to_element(self, element: WebElement):
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

    def create_selector(self, element: WebElement) -> Select:
        return Select(element)

    def select_by_text(self, text: str, element: Select) -> bool:
        try:
            element.select_by_visible_text(text)
            return True
        except NoSuchElementException:
            print("NoSuchElementException")
            return False

    def close(self):
        self.driver.close()
