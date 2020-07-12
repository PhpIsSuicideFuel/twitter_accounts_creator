import sys
import os
import json
import importlib
import time
from sys import path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from TwitterHandler import TwitterHandler
from pva.PvaApi import PvaApi
import constants.javascript_constants as javascript_constants

WEBDRIVER_PATH = os.getcwd() + "\\webdriver\\chromedriver.exe"
PROXY_FILE_PATH = None
ACCOUNTS_FILE_PATH = os.getcwd() + "accounts" + \
    datetime.now().strftime("%Y-%m-%d %H:%M:%S")

AVAILABLE_PVA_SERVICES = {}


class TwitterCreator:
    pva_services = []

    def __init__(self):
        self.pva = self.get_cheapest_service()

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
            if "proxy_file" in config_data:
                global PROXY_FILE_PATH
                PROXY_FILE_PATH = os.getcwd() + config_data.get("proxy_file")
            if "accounts_file" in config_data:
                global ACCOUNTS_FILE_PATH
                ACCOUNTS_FILE_PATH = os.getcwd() + config_data.get("accounts_file")

    def get_cheapest_service(self):
        pva_services_with_balance = [
            service for service in self.pva_services if service.balance > service.service_price]
        return min(pva_services_with_balance,
                   key=lambda service: service.service_price)

    def start(self):
        proxies = []

        if PROXY_FILE_PATH is not None:
            with open(PROXY_FILE_PATH, mode='r') as proxy_file:
                proxies = [line.strip('\n') for line in proxy_file]

        proxies = iter(proxies)
        self.twitter = TwitterHandler(
            get_web_driver(next(proxies, None)), self.pva)

        with open(ACCOUNTS_FILE_PATH, mode='a') as accounts_file:
            while True:
                proxy = next(proxies, None)
                account = self.twitter.create_account()
                accounts_file.write(
                    f"{account.get('username')} : {account.get('password')} | {proxy}")
                self.twitter.driver = get_web_driver(proxy)

        print(account)
        print('hoi')


def get_web_driver(proxy=None):
    launch_chrome()
    chrome_options = Options()
    # note that the port numbers should match
    chrome_options.add_experimental_option(
        "debuggerAddress", "127.0.0.1:9222")

    if proxy is not None:
        chrome_options.add_argument(f"--proxy-server={proxy}")

    try:
        driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)
    except WebDriverException as e:
        raise SystemExit(e)

    for script in javascript_constants.SCRIPTS:
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument", {"source": script})

    driver.delete_all_cookies()

    return driver


def launch_chrome(debug_port=9222):
    os.system('taskkill /F /im chrome.exe')
    os.system(
        f'start chrome --remote-debugging-port={debug_port} --user-data-dir=remote-profile --no-sandbox')
    print("chrome started")


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

    creator = TwitterCreator()
    creator.start()

    print('Process ended')


if __name__ == "__main__":
    main(None)
