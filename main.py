# python accounts.py -i ../../data/twitter-creator.json -d regular -f 1
# python accounts.py -i ../../data/twitter-creator.json -d proxy -f 1
import sys
import os
import time
import getopt
import webbrowser
import importlib
import random
from SmsHelper import smsHelper
from subprocess import call
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from SeleniumHelper import SeleniumHelper
from TwitterHandler import TwitterHandler
import constants.javascript_constants as javascript_constants

WEBDRIVER_PATH = os.getcwd() + "\webdriver\chromedriver.exe"

class TwitterCreator:

    def __init__(self):
        browser = self.get_web_driver()
        browser.delete_all_cookies()
        self.twitter = TwitterHandler(browser)

    def mobileCreateUser(self, row):
        self.browser.loadPage(self.DESKTOP_URL_CREATE)
        self.waitAndWrite(self.DESKTOP_FIELD_SIGN_UP_NAME, row['name'])
        self.submitForm(self.selectAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_EMAIL, row['email']))
        self.submitForm(self.waitAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_PASSWORD, row['password']))
        self.clickSelector(self.DESKTOP_BUTTON_SKIP_PHONE)
        self.submitForm(self.waitAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_USERNAME, row['username']))
        self.waitAndClick(self.DESKTOP_BUTTON_INTERESTS)
        #main_content > div.footer > form > input
        time.sleep(9999)
        # self.submitForm()

    def desktopCreateUser(self, row):
        self.loadPage(self.DESKTOP_URL_CREATE)
        self.waitAndWrite(self.DESKTOP_FIELD_SIGN_UP_NAME, row['name'])
        self.selectAndWrite(self.DESKTOP_FIELD_SIGN_UP_EMAIL, row['email'])
        self.submitForm(self.selectAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_PASSWORD, row['password']))
        self.waitShowElement(self.DESKTOP_PAGE_CONTAINER)
        self.loadPage(self.DESKTOP_URL_SKIP)
        self.submitForm(self.waitAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_USERNAME, row['username']))
        self.waitShowElement(self.DESKTOP_PAGE_CONTAINER)
        self.loadPage(self.DESKTOP_URL_MAIN)
        time.sleep(9999)

    def desktopCreateUserPhone(self, row):
        self.loadPage(self.DESKTOP_URL_CREATE)
        self.waitAndWrite(self.DESKTOP_FIELD_SIGN_UP_NAME, row['name'])
        self.selectAndWrite(self.DESKTOP_FIELD_SIGN_UP_EMAIL, row['email'])
        self.submitForm(self.selectAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_PASSWORD, row['password']))
        self.submitForm(self.waitAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_PHONE, row['phone']))
        row['code'] = input('Code: ')
        self.submitForm(self.waitAndWrite(
            self.DESKTOP_FIELD_SIGN_UP_CODE, row['code']))
        self.waitAndClick(self.DESKTOP_FIELD_SIGN_UP_SUGGESTION)
        self.submitFormSelector(self.DESKTOP_FIELD_SIGN_UP_USERNAME)
        self.waitShowElement(self.DESKTOP_PAGE_CONTAINER)
        self.loadPage(self.DESKTOP_URL_MAIN)
        self.submitForm(self.waitShowElement(self.DESKTOP_FIELD_LOGOUT))
        self.waitShowElement(self.DESKTOP_PAGE_INI)

    def start(self, callbacks, inputFile, fromRow, toRow, driverType, pva):
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

    def get_web_driver(self, driverType="proxy"):
        if driverType == 'proxy':
            chrome_options = Options()
            # Note the port numbers should match.
            chrome_options.add_experimental_option(
                "debuggerAddress", "127.0.0.1:9222")
            driver = webdriver.Chrome(WEBDRIVER_PATH, options=chrome_options)
            for script in javascript_constants.SCRIPTS:
                driver.execute_cdp_cmd(
                    "Page.addScriptToEvaluateOnNewDocument", {"source": script})
            return driver
            # profile = webdriver.FirefoxProfile()
            # profile.set_preference("network.proxy.type", 1)
            # profile.set_preference("network.proxy.socks", "127.0.0.1")
            # profile.set_preference("network.proxy.socks_port", 9150)
            # profile.set_preference("network.proxy.socks_remote_dns", True)
            # profile.set_preference("places.history.enabled", False)
            # profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
            # profile.set_preference("privacy.clearOnShutdown.passwords", True)
            # profile.set_preference(
            #     "privacy.clearOnShutdown.siteSettings", True)
            # profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
            # profile.set_preference("signon.rememberSignons", False)
            # profile.set_preference("network.cookie.lifetimePolicy", 2)
            # profile.set_preference("network.dns.disablePrefetch", True)
            # profile.set_preference("network.http.sendRefererHeader", 0)
            # profile.set_preference("javascript.enabled", False)
            # profile.set_preference("permissions.default.image", 2)
            # return webdriver.Firefox(profile)
        elif driverType == 'headless':
            return webdriver.PhantomJS()
        else:
            return webdriver.Firefox()


def main(argv):
    print(WEBDRIVER_PATH)
    os.system('taskkill /F /im chrome.exe')
    os.system(
        'start chrome --remote-debugging-port=9222 --user-data-dir=remote-profile --no-sandbox')
    fromRow = 1
    toRow = -1
    inputFile = None
    driverType = 'proxy'
    # opts, args = getopt.getopt(argv, "f:t:i:d:")
    # if opts:
    #     for o, a in opts:
    #         if o in ("-f"):
    #             fromRow = int(a)
    #         elif o in ("-t"):
    #             toRow = int(a)
    #         elif o in ("-i"):
    #             inputFile = a
    #         elif o in ("-d"):
    #             driverType = a
    # while not inputFile:
    #     inputFile = input('Input file path: ')
    creator = TwitterCreator()
    pva = smsHelper()
    print('Process started')
    creator.start(callbacks=[creator.desktopCreateUserPhone],
                  inputFile=inputFile, fromRow=fromRow, toRow=toRow, driverType=driverType, pva=pva)
    print('Process ended')


if __name__ == "__main__":
    main(None)
