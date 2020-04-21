import requests
import time
import re
import sys

BASE_URL = 'https://admin.smscodes.io/api/sms/'
API_KEY = 'a02975e0-b00b-46b1-97e0-f8a16e47a4a5'
SERVICE_ID = '36ea908b-6b20-4573-9faa-74924b3bcd7f'
COUNTRY = 'RU'

class smsHelper:

    def __init__(self):
        self.currentBalance = self.getBalance()

    def getBalance(self):
        payload = {'key': API_KEY}
        try:
            r = requests.get(BASE_URL + 'GetBalance',
                             params=payload).json()
        except:
            r = None
        if r is not None and r['Status'] == 'Success':
            return r['Balance']
        return None

    def getPhoneNumber(self):
        payload = {'key': API_KEY, 'iso': COUNTRY, 'serv': SERVICE_ID}
        try:
            r = requests.get(BASE_URL + 'GetServiceNumber',
                             params=payload).json()
        except:
            r = None
        if r is not None and r['Status'] == 'Success':
            self.number = r['Number']
            self.securityId = r['SecurityId']
            print('iso: {0}, service: {1}, rate: {2}'.format(
                r['ISO'], r['Service'], r['Rate']))
        return '+' + self.number

    def getSmsCode(self):
        payload = {'key': API_KEY,
                   'sid': self.securityId, 'number': self.number}
        try:
            r = requests.get(BASE_URL + 'GetSMSCode', params=payload).json()
        except:
            r = None
            self.code = None

        print(r)

        if r['Error'] == 'InsufficientBalance':
            print('Insufficient balance, terminating.')
            sys.exit()
        if r is not None and r['Status'] == 'Success':
            self.code = r['SMS']
            self.currentBalance = r['Balance']

        return

    def phoneVerification(self):
        for i in range(0, 12):
            self.getSmsCode()
            print('iteration: {0}, code: {1}'.format(i, self.code))
            if self.code != 'Message not received yet':
                break
            time.sleep(10)

        if self.code != 'Message not received yet':
            try:
                # regex to extract code
                self.code = re.search('(^\d+)', self.code).group(1)
            except AttributeError:
                self.code = None
            return self.code
        else:
            return None


print('')


def main():
    helper = smsHelper()
    print(helper.getPhoneNumber())
    # print(helper.getPhoneNumber())
    # print(helper.securityId)
    #kodas = helper.phoneVerification()
    # if kodas is None:
    #     print('kodas yra none')
    # else:
    #     print(kodas)


if __name__ == "__main__":
    main()
