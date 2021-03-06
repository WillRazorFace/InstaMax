from platform import system

OPTIONS_FILE = 'instamax_config'

if system() == 'Windows':
    CLEAR_CONSOLE_COMMAND = 'cls'
elif system() == 'Linux':
    CLEAR_CONSOLE_COMMAND = 'clear'

BANNER = '''
    ____                   __             __  ___                
   /  _/   ____    _____  / /_  ____ _   /  |/  /  ____ _   _  __
   / /    / __ \  / ___/ / __/ / __ `/  / /|_/ /  / __ `/  | |/_/
 _/ /    / / / / (__  ) / /_  / /_/ /  / /  / /  / /_/ /  _>  <  
/___/   /_/ /_/ /____/  \__/  \__,_/  /_/  /_/   \__,_/  /_/|_|  
'''

DRIVER_MENU = '''
[1] - Chrome
[2] - Firefox
[3] - Safari
'''

MAIN_MENU = '''
[0] - Reconfigure credentials and driver
[1] - Follow suggested
[2] - Like posts from feed
[3] - Like posts from hashtag
[4] - Get followers from an account
[5] - Search follower in an account
[6] - Get following users from an account
[7] - Search following user in an account
[8] - Search not followers
[9] - Unfollow not followers
[10] - Unfollow'''
