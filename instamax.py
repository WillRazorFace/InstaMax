from core.instabot import Bot
from core.menu import *
from core.exceptions import *
from os import system, path, remove
from platform import system as sys_os
from typing import Type
from time import sleep

OPTIONS_FILE = '.options'
if sys_os() == 'Windows':
    CLEAR_CONSOLE_COMMAND = 'cls'
elif sys_os() == 'Linux':
    CLEAR_CONSOLE_COMMAND = 'clear'

def configure() -> None:
    driver_options = {'1': 'chrome', '2': 'firefox', '3': 'safari'}

    system(CLEAR_CONSOLE_COMMAND)
    print('Enter your Instagram account username: ', end='')
    username = input()
    print('Enter your Instagram account password: ', end='')
    password = input()
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        print(DRIVER_MENU)
        driver = input('>>> ')
        
        try:
            driver = driver_options[driver]
            system(CLEAR_CONSOLE_COMMAND)

            while True:
                print('Enter the path to your driver (/example/driver/path/driver.exe): ', end='')
                driver_path = input('')

                if path.isfile(driver_path):
                    break
                else:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid path, file does not exist\n')
                    continue
            
            break
        except KeyError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option\n')
            continue

    with open(OPTIONS_FILE, 'w') as file:
        file.write(username + '\n' + password + '\n' + driver + '\n' + driver_path)

def follow_suggested() -> int:
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        print('How many users do you want to follow? (numbers only) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)

            while True:
                ignore = []
                print("Are there any accounts you don't want to follow? (Y/N) ", end='')
                dont_follow = input()

                if dont_follow == 'Y' or dont_follow == 'y':
                    while True:
                        print(f'{len(ignore)} accounts to not follow\n')
                        print('Enter the account username (type "exit" to stop): ', end='')
                        
                        username = input()

                        if username == 'exit':
                            break
                        
                        ignore.append(username)
                        continue
                elif dont_follow == 'N' or dont_follow == 'n':
                    break
                else:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid option')
                    continue
                
                break

            break        
        except ValueError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid quantity\n')
            continue
    
    system(CLEAR_CONSOLE_COMMAND)
    print('Following')
    followed = insta_bot.follow_suggested(quantity, ignore)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{followed} users followed. Press anything to return to the menu.', end='')
    input()

if not path.isfile(OPTIONS_FILE):
    configure()
else:
    try:
        with open(OPTIONS_FILE, 'r') as file:
            lines = [line.strip('\n') for line in file.readlines()]

            username = lines[0]
            password = lines[1]
            driver = lines[2]
            driver_path = lines[3]
    except IndexError:
        remove(OPTIONS_FILE)
        system(CLEAR_CONSOLE_COMMAND)
        print('Invalid options file removed. Run the script again to reconfigure.')
        exit(1)

insta_bot = Bot(username, password, driver, driver_path)

try:
    system(CLEAR_CONSOLE_COMMAND)
    print('Trying to log in...')
    insta_bot.login()
except InvalidCredentials:
    insta_bot.close_browser()
    system(CLEAR_CONSOLE_COMMAND)
    print('Invalid credentials, not logged in. Aborting.')
    exit(1)

options = {'0': configure, '1': follow_suggested}

while True:
    system(CLEAR_CONSOLE_COMMAND)
    print(BANNER)
    print(f'Logged as {insta_bot.usuario}')
    print(MAIN_MENU)
    option = input('\n>>> ')

    try:
        options[option]()
        continue
    except KeyError:
        system(CLEAR_CONSOLE_COMMAND)
        print('Invalid option')
        sleep(3)
        continue
