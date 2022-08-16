from stdiomask import getpass
from os import path

EMAIL = 'email'
PASSWORD = 'password'
IRCC = 'ircc'
BIRTHDAY = 'birthday'
TELEGRAM_KEY = 'telegram_key'
MESSAGE_ID = 'message_id'


def user_init() -> dict[str, str]:
    if not path.exists("userInfo.txt"):
        print("User init")
        print("--------")
        print()
        user_data = {}
        user_data.update([
            (EMAIL, str(input("Enter Your Email: "))),
            (PASSWORD, str(getpass("Enter Your Password: "))),
            (IRCC, str(input("Enter Your IRCC No.: "))),
            (BIRTHDAY, str(input("Enter Your Birthday like year-month-day: "))),
            (TELEGRAM_KEY, str(input("Enter Your Telegram Api key: "))),
            (MESSAGE_ID, str(input("Enter Your Telegram Api Message Id: ")))
        ])
        add_user_info(user_data)
    return get_user_info()


def get_user_info() -> dict[str, str]:
    users_info = {}
    with open('userInfo.txt', 'r') as file:
        for line in file:
            line = line.split()
            users_info.update({line[0]: line[1]})

    return users_info


def add_user_info(user_info: dict) -> None:
    with open('userInfo.txt', 'a') as file:
        for info in user_info:
            file.write(info)
            file.write(' ')
            file.write(user_info[info])
            file.write('\n')

