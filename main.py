import sys
import os
import random
import json
import importlib
import time
from sys import path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from TwitterHandler import TwitterHandler
from pva.PvaApi import PvaApi
import constants.javascript_constants as javascript_constants

WEBDRIVER_PATH = os.getcwd() + "\\webdriver\\chromedriver.exe"

AVAILABLE_PVA_SERVICES = {
}


class TwitterCreator:
    pva_services = []

    def __init__(self):
        browser = self.get_web_driver()
        browser.delete_all_cookies()
        pva = self.get_cheapest_service()
        self.twitter = TwitterHandler(browser, pva)

    @classmethod
    def read_configuration(cls, config_file_name="config.json"):
        with open(config_file_name) as config_file:
            config_data = json.load(config_file)
            for pva_service in config_data.get("pva_services"):
                pva = AVAILABLE_PVA_SERVICES.get(pva_service["name"])
                if pva is None:
                    print(
                        f"Unknown service: \"{pva_service['name']}\" specified in {config_file_name}")
                    sys.exit()
                cls.pva_services.append(
                    pva(pva_service["base_url"],
                        pva_service["api_key"],
                        pva_service["service_id"],
                        pva_service["country"]))
            if "webdriver_path" in config_data:
                global WEBDRIVER_PATH
                WEBDRIVER_PATH = os.getcwd() + config_data.get("webdriver_path")

    def get_cheapest_service(self):
        pva_services_with_balance = [
            service for service in self.pva_services if service.balance > service.service_price]
        return min(pva_services_with_balance,
                   key=lambda service: service.service_price)

    def start(self):
        account = self.twitter.create_account()
        # TODO clean user data after account creation
        print(account)
        print('hoi')
        # try:
        #     rows = simplejson.loads(open(inputFile).read())
        #     numElements = len(rows)
        # except:
        #     numElements = 0
        # if numElements > 0:
        #     if toRow == -1:
        #         toRow = numElements
        #     else:
        #         if toRow > numElements:
        #             toRow = numElements
        #     fromRow -= 1
        #     if fromRow < numElements:
        #         self.driver = self.getWebdriver(driverType)
        #         for numRow in range(fromRow, toRow):
        #             row = rows[numRow]
        #             print('Processing row: ' + str(numRow))
        #             for callback in callbacks:
        #                 callback(row)
        #             print('Processed.')
        #         self.close()
        #     else:
        #         print('Index out of bounds')
        # else:
        #     print('Data could not be extracted')

    def get_web_driver(self):
        chrome_options = Options()
        # Note the port numbers should match.
        chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9222")
        try:
            driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)
        except WebDriverException as e:
            raise SystemExit(e)

        for script in javascript_constants.SCRIPTS:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument", {"source": script})
        return driver


def load_pva_modules():
    module_path = os.getcwd() + "\\pva"
    path.append(module_path)
    for module_name in os.listdir(module_path):
        if module_name != "PvaApi.py" and module_name.endswith(".py"):
            module_name = module_name[:-3]

            try:
                module = importlib.import_module(module_name)
            except ImportError:
                print("Couldn't import", module_name)
                continue

            pva_class = getattr(module, module_name)
            if isinstance(pva_class, type) and issubclass(pva_class, PvaApi):
                global AVAILABLE_PVA_SERVICES
                AVAILABLE_PVA_SERVICES.update({module_name: pva_class})
            else:
                print(f"Pva module {module_name} has to derive from PvaApi")


def main(argv):
    load_pva_modules()
    print(AVAILABLE_PVA_SERVICES)
    TwitterCreator.read_configuration()
    os.system('taskkill /F /im chrome.exe')
    os.system(
        'start chrome --remote-debugging-port=9222 --user-data-dir=remote-profile --no-sandbox')
    print("chrome started")

    creator = TwitterCreator()

    # creator.start()
    # TwitterCreator.pva_services[0].add_number()
    # print(TwitterCreator.pva_services[0].g())

    # creator.start()
    print('Process ended')


if __name__ == "__main__":
    main(None)
