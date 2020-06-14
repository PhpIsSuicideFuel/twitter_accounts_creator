DESKTOP_URL_CREATE = 'https://twitter.com/signup'

DESKTOP_FIELD_SIGN_UP_NAME = """//input[@name='name']"""
DESKTOP_FIELD_SIGN_UP_PASSWORD = """//input[@name='password' and @type='password']"""
DESKTOP_FIELD_SIGN_UP_PHONE = """//input[@name='phone_number']"""
DESKTOP_FIELD_SIGN_UP_CODE = """//input[@name='verfication_code']"""
DESKTOP_FIELD_SIGN_UP_SUGGESTION = '.suggestions > ul:nth-child(2) > li:nth-child(1) > button:nth-child(1)'
DESKTOP_FIELD_LOGOUT = '#signout-form'

DESKTOP_BUTTON_SKIP_FOR_NOW = """//div[@data-focusable='true' and @tabindex='0']/div/span/span[text()='Skip for now']//ancestor::div[2]"""
DESKTOP_BUTTON_NEXT = """//div[@data-focusable='true' and @tabindex='0']/div/span/span[text()='Next']//ancestor::div[2]"""
DESKTOP_BUTTON_OK = """//div[@data-focusable='true' and @tabindex='0']/div/span/span[text()='OK']//ancestor::div[2]"""
DESKTOP_BUTTON_SIGN_UP = """//div[@role='button' and @data-focusable='true' and @tabindex='0']/div/span/span[text()='Sign up']"""
