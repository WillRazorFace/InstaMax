from core.instabot import Bot
from os import system, path
from .constants import CLEAR_CONSOLE_COMMAND, OPTIONS_FILE, DRIVER_MENU
from time import sleep

def configure() -> tuple:
    driver_options = {'1': 'chrome', '2': 'firefox', '3': 'safari'}

    system(CLEAR_CONSOLE_COMMAND)
    print('Enter your Instagram account username: @', end='')
    username = input()
    print('Enter your Instagram account password: ', end='')
    password = input()
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        print('Select your driver model')
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

    return username, password, driver, driver_path

def follow_suggested(bot_instance: Bot) -> int:
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
                    system(CLEAR_CONSOLE_COMMAND)

                    while True:
                        print('[1] - Get accounts from a file (one user per line)\n[2] - Insert accounts one by one\n')
                        accounts_input = input('>>> ')

                        if accounts_input == '1':
                            system(CLEAR_CONSOLE_COMMAND)

                            while True:
                                print('Enter the path to the file (example/path/to/the/file): ', end='')
                                file_path = input()

                                if path.isfile(file_path):
                                    with open(file_path, 'r') as file:
                                        for account in file.readlines():
                                            ignore.append(account)
                                        
                                    break
                                else:
                                    system(CLEAR_CONSOLE_COMMAND)
                                    print('Invalid path\n')
                                    continue
                            
                            break
                        elif accounts_input == '2':
                            system(CLEAR_CONSOLE_COMMAND)
                            print(f'{len(ignore)} accounts to not follow\n')
                            print('Enter the account username (type "exit" to stop): ', end='')
                                    
                            username = input()

                            if username == 'exit':
                                break
                                    
                            ignore.append(username)
                            continue
                        else:
                            system(CLEAR_CONSOLE_COMMAND)
                            print('Invalid option\n')
                            continue
                elif dont_follow == 'N' or dont_follow == 'n':
                    break
                else:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid option\n')
                    continue
                    
                break

            break        
        except ValueError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid quantity\n')
            continue
        
    system(CLEAR_CONSOLE_COMMAND)
    print('Following')
    followed = bot_instance.follow_suggested(quantity, ignore)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{followed} users followed. Press anything to return to the menu.', end='')
    input()

def like_feed(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        print('How many posts from feed do you want to like? (numbers only) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)
        except ValueError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid quantity\n')
            continue
        
        break

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Liking posts from your feed')
    liked_posts = bot_instance.like_feed_posts(quantity)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{liked_posts} posts liked. Press anything to return to the menu.', end='')
    input()

def like_posts(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        print('How many posts do you want to like? (numbers only) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)

            print('Enter the posts hashtag: #', end='')
            hashtag = input()
        except ValueError:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid quantity\n')
            continue
        
        break

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Liking posts from #{hashtag}')
    liked_posts = bot_instance.like_posts_by_hashtag(hashtag, quantity)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{liked_posts} posts liked. Press anything to return to the menu.', end='')
    input()

def get_followers(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)
    all = False

    while True:
        print('Enter the instagram account username: @', end='')
        account = input()

        print('How many followers you want to get? (numbers only) (type "all" to get all followers) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)
        except ValueError:
            if quantity == 'all' or quantity == 'All' or quantity == 'ALL':
                all = True
            else:
                system(CLEAR_CONSOLE_COMMAND)
                print('Invalid quantity\n')
                continue
        
        break

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Searching for followers of {account}')
    followers = [follower for follower in bot_instance.get_followers(account, quantity, all)]

    while True:
        system(CLEAR_CONSOLE_COMMAND)
        
        for follower in followers:
            print(follower)

        print(f'\n{len(followers)} followers found on @{account}. Do you want to save this information into a file? (Y/N) ', end='')
        save = input()

        if save == 'Y' or save == 'y':
            while True:
                print('\nEnter the path for the file to be saved: ', end='')
                path = input()

                try:
                    with open(path, 'w') as file:
                        for follower in followers:
                            file.write(follower + '\n')
                except FileNotFoundError:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid path')
                    continue
                
                break
            
            print(f'Information saved in {path}. Press anything to return to menu.', end='')
            input()
            break
        elif save == 'N' or save == 'n':
            print('\nNo information saved. Press anything to return to menu.', end='')
            input()
            break
        else:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            continue

def search_follower(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)

    print('Enter the account to be searched: @', end='')
    search_account = input()
    print('Enter the account to be found: @', end='')
    account = input()

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Searching for @{account} in @{search_account} list of followers')
    is_follower = bot_instance.search_follower(search_account, account)

    if is_follower:
        print(f'Found. @{account} is following @{search_account}. Press anything to return to menu.', end='')
        input()
    else:
        print(f'Not found. @{account} is not following @{search_account}. Press anything to return to menu.', end='')
        input()

def get_following(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)
    all = False

    while True:
        print('Enter the instagram account username: @', end='')
        account = input()

        print('How many following users you want to get? (numbers only) (type "all" to get all following users) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)
        except ValueError:
            if quantity == 'all' or quantity == 'All' or quantity == 'ALL':
                all = True
            else:
                system(CLEAR_CONSOLE_COMMAND)
                print('Invalid quantity\n')
                continue
        
        break

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Searching for following users in @{account}')
    following = [user for user in bot_instance.get_following(account, quantity, all)]

    while True:
        system(CLEAR_CONSOLE_COMMAND)

        for user in following:
            print(user)

        print(f'\n{len(following)} following users found on @{account}. Do you want to save this information into a file? (Y/N) ', end='')
        save = input()

        if save == 'Y' or save == 'y':
            while True:
                print('\nEnter the path for the file to be saved: ', end='')
                path = input()

                try:
                    with open(path, 'w') as file:
                        for user in following:
                            file.write(user + '\n')
                except FileNotFoundError:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid path')
                    continue
                
                break
            
            print(f'Information saved in {path}. Press anything to return to menu.', end='')
            input()
            break
        elif save == 'N' or save == 'n':
            print('\nNo information saved. Press anything to return to menu.', end='')
            input()
            break
        else:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            continue

def search_following(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)

    print('Enter the account to be searched: @', end='')
    search_account = input()
    print('Enter the account to be found: @', end='')
    account = input()

    system(CLEAR_CONSOLE_COMMAND)
    print(f'Searching for @{account} in @{search_account} list of following users')
    is_following = bot_instance.search_following(search_account, account)

    if is_following:
        print(f'Found. @{account} is followed by @{search_account}. Press anything to return to menu.', end='')
        input()
    else:
        print(f'Not found. @{account} is not followed by @{search_account}. Press anything to return to menu.', end='')
        input()

def search_not_followers(bot_instance: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)
    print('Searching for not followers')
    not_followers = bot_instance.search_not_followers()

    while True:
        system(CLEAR_CONSOLE_COMMAND)

        for user in not_followers:
            print(user)

        print(f'\n{len(not_followers)} not followers found on your account. Do you want to save this information into a file? (Y/N) ', end='')
        save = input()

        if save == 'Y' or save == 'y':
            while True:
                print('\nEnter the path for the file to be saved: ', end='')
                path = input()

                try:
                    with open(path, 'w') as file:
                        for not_follower in not_followers:
                            file.write(not_follower + '\n')
                except FileNotFoundError:
                    system(CLEAR_CONSOLE_COMMAND)
                    print('Invalid path')
                    continue
                
                break
            
            print(f'Information saved in {path}. Press anything to return to menu.', end='')
            input()
            break
        elif save == 'N' or save == 'n':
            print('\nNo information saved. Press anything to return to menu.', end='')
            input()
            break
        else:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            continue

def unfollow_not_followers(bot_instace: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)

    while True:
        ignore = []
        print("Are there any accounts you don't want to unfollow? (Y/N) ", end='')
        dont_unfollow = input()

        if dont_unfollow == 'Y' or dont_unfollow == 'y':
            while True:
                system(CLEAR_CONSOLE_COMMAND)
                print(f'{len(ignore)} accounts to not follow\n')
                print('Enter the account username (type "exit" to stop): ', end='')
                        
                username = input()

                if username == 'exit':
                    break
                        
                ignore.append(username)
                continue
        elif dont_unfollow == 'N' or dont_unfollow == 'n':
            break
        else:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            continue
                
        break
    
    system(CLEAR_CONSOLE_COMMAND)
    print('Unfollowing not followers')
    unfollowed = bot_instace.unfollow_not_followers(ignore)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{unfollowed} not followers unfollowed. Press anything to return to menu.', end='')
    input()

def unfollow(bot_instace: Bot) -> None:
    system(CLEAR_CONSOLE_COMMAND)
    all = False

    while True:
        print('How many following users you want to unfollow? (numbers only) (type "all" to unfollow all users except those you specify) ', end='')
        quantity = input()

        try:
            quantity = int(quantity)
        except ValueError:
            if quantity == 'all' or quantity == 'All' or quantity == 'ALL':
                all = True
            else:
                system(CLEAR_CONSOLE_COMMAND)
                print('Invalid quantity\n')
                continue
        
        break

    while True:
        ignore = []
        print("Are there any accounts you don't want to unfollow? (Y/N) ", end='')
        dont_unfollow = input()

        if dont_unfollow == 'Y' or dont_unfollow == 'y':
            while True:
                system(CLEAR_CONSOLE_COMMAND)
                print(f'{len(ignore)} accounts to not unfollow\n')
                print('Enter the account username (type "exit" to stop): ', end='')
                        
                username = input()

                if username == 'exit':
                    break
                        
                ignore.append(username)
                continue
        elif dont_unfollow == 'N' or dont_unfollow == 'n':
            break
        else:
            system(CLEAR_CONSOLE_COMMAND)
            print('Invalid option')
            continue
                
        break

    system(CLEAR_CONSOLE_COMMAND)
    print('Unfollowing')
    unfollowed = bot_instace.unfollow(quantity, ignore, all)

    system(CLEAR_CONSOLE_COMMAND)
    print(f'{unfollowed} unfollowed users. Press anything to return to menu.', end='')
    input()
