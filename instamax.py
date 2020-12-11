try:
    from core.instabot import Bot
    from menu.constants import MAIN_MENU, OPTIONS_FILE, CLEAR_CONSOLE_COMMAND, BANNER
    from menu.functions import (
        configure,
        follow_suggested,
        like_posts,
        get_followers,
        search_follower,
        get_following,
        search_following,
        search_not_followers,
        unfollow_not_followers,
        unfollow
    )
    
    from core.exceptions import InvalidCredentials
    from os import system, path, remove
    from platform import system as sys_os
    from typing import Type
    from time import sleep
    
    if not path.isfile(OPTIONS_FILE):
        username, password, driver, driver_path = configure()
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

    options = {
        '0': configure,
        '1': follow_suggested,
        '2': like_posts,
        '3': get_followers,
        '4': search_follower,
        '5': get_following,
        '6': search_following,
        '7': search_not_followers,
        '8': unfollow_not_followers,
        '9': unfollow,
    }

    while True:
        system(CLEAR_CONSOLE_COMMAND)
        print(BANNER)
        print(f'Logged as @{insta_bot.usuario}')
        print(MAIN_MENU)
        option = input('\n>>> ')

        try:
            if option == '0':
                username, password, driver, driver_path = options[option]()
                insta_bot.close_browser()
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

                continue
            
            options[option](insta_bot)
            continue
        except KeyError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            sleep(3)
            continue
except KeyboardInterrupt:
    system(CLEAR_CONSOLE_COMMAND)
    print('Exiting...')
