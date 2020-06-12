import sys
import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from TwitterHandler import TwitterHandler
from pva.SmsPvaApi import SmsPvaApi
from pva.SmsCodesApi import SmsCodesApi
import constants.javascript_constants as javascript_constants

WEBDRIVER_PATH = os.getcwd() + r"\webdriver\chromedriver.exe"

AVAILABLE_PVA_SERVICES = {
    "SmsPva": SmsPvaApi,
    "SmsCodes": SmsCodesApi
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
            for pva_service in config_data["pva_services"]:
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

    def get_cheapest_service(self):
        return min(self.pva_services,
                   key=lambda service: service.service_price)

    def start(self):
        self.twitter.create_account('asd', 'asd', None)
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
        driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)
        for script in javascript_constants.SCRIPTS:
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument", {"source": script})
        return driver


def main(argv):
    TwitterCreator.read_configuration()
    os.system('taskkill /F /im chrome.exe')
    os.system(
        'start chrome --remote-debugging-port=9222 --user-data-dir=remote-profile --no-sandbox')
    print("chrome started")

    # creator = TwitterCreator()

    print(TwitterCreator.pva_services[1].get_balance())
    # creator.start()
    print('Process ended')


if __name__ == "__main__":
    main(None)
