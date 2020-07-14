## Twitter accounts creator
A python program written using selenium to automate twitter accounts creation with phone verification.

## How to use
Download chromedriver here: https://chromedriver.chromium.org/downloads
### Configuration file
Before using you have to setup a configuration file "config.json".
Example:
```
{
    "pva_services": [
        {
            "name": "SmsCodes",
            "base_url": "https://admin.smscodes.io/api/sms/",
            "api_key": "YOURAPIKEY",
            "service_id": "36ea908b-6b20-4573-9faa-74924b3bcd7f",
            "country": "RU"
        },
        {
            "name": "SmsPva",
            "base_url": "http://smspva.com/priemnik.php",
            "api_key": "YOURAPIKEY",
            "service_id": "opt41",
            "country": "RU"
        }
    ],
    "webdriver_path": "\\webdriver\\chromedriver.exe",
    "proxy_file": "\\proxy.txt"
}
```

- **"pva_services"** - a list of modules of pva services you intend to use to verify your accounts.
- **"webdriver_path"** - relative path to your chromedriver, default is \webdriver\chromedriver.exe.
- **"proxy_file"** - relative path to a text file filled with proxies you want to use, if its not specified no proxies will be used.

### Proxy file format
All of the proxies have to be formatted correctly and each proxy must be on a new line
```
proxy-scheme://proxy-ip:proxy-port
```

### Account information storing
All created accounts will be stored in a .txt file named "accounts--*current-datetime*"

## Creating other pva modules
You can easily add support for other pva services by creating a new pva module, just make it a subclass of PvaApi and use the already created modules for reference.
