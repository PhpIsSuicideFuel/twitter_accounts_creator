
MOBILE_URL_CREATE = 'https://mobile.twitter.com/signup?type=email'
MOBILE_FIELD_SIGN_UP_NAME = '#oauth_signup_client_fullname'
MOBILE_FIELD_SIGN_UP_EMAIL = '#oauth_signup_client_phone_number'
MOBILE_FIELD_SIGN_UP_PASSWORD = '#password'
MOBILE_FIELD_SIGN_UP_USERNAME = '#custom_name'
MOBILE_BUTTON_SKIP_PHONE = '.signup-skip input'
MOBILE_BUTTON_INTERESTS = 'input[data-testid="Button"]'

DESKTOP_URL_CREATE = 'https://twitter.com/signup'
DESKTOP_URL_SKIP = 'https://twitter.com/account/add_username'
DESKTOP_URL_MAIN = 'https://twitter.com'
DESKTOP_FIELD_SIGN_UP_NAME = """//input[@name='name']"""
DESKTOP_FIELD_SIGN_UP_EMAIL = '#email'
DESKTOP_FIELD_SIGN_UP_PASSWORD = '#password'
DESKTOP_FIELD_SIGN_UP_USERNAME = '#username'
DESKTOP_FIELD_SIGN_UP_PHONE = """//input[@name='phone_number']"""
DESKTOP_FIELD_NEXT = """//div[@data-focusable='true' and @tabindex='0']/div/span/span[text()='Next']//ancestor::div[2]"""
DESKTOP_FIELD_OK = """//div[@data-focusable='true' and @tabindex='0']/div/span/span[text()='OK']//ancestor::div[2]"""
DESKTOP_FIELD_SIGN_UP = """//div[@role='button' and @data-focusable='true' and @tabindex='0']/div/span/span[text()='Sign up']"""
DESKTOP_FIELD_SIGN_UP_CODE = """//input[@name='verfication_code']"""
DESKTOP_FIELD_SIGN_UP_SUGGESTION = '.suggestions > ul:nth-child(2) > li:nth-child(1) > button:nth-child(1)'
DESKTOP_FIELD_LOGOUT = '#signout-form'
DESKTOP_BUTTON_SKIP_PHONE = '.signup-skip input'
DESKTOP_BUTTON_CALL_ME = 'input[name="call_me"]'
DESKTOP_BUTTON_INTERESTS = 'input[data-testid="Button"]'

DESKTOP_PAGE_CONTAINER = '#page-container'
DESKTOP_PAGE_PHONE = '.PageContainer'
DESKTOP_PAGE_INI = '#doc'
