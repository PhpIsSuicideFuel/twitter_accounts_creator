import secrets
import random
import json
import string

symbols = string.ascii_letters + string.digits
names = json.loads(open("names.json").read())


def generate_password():
    return ''.join(secrets.choice(symbols) for _ in range(15))


def generate_username():
    return random.choice(names) + str(random.randint(0, 100))
