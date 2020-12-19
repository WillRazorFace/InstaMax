from selenium import webdriver
from selenium.webdriver.remote import webelement
from os import devnull
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    ElementClickInterceptedException,
    TimeoutException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from . import exceptions
from time import sleep
from typing import Iterator, Iterable, List

class Bot:
    INSTAGRAM_URL: str = 'https://www.instagram.com/'

    def __init__(self, user: str, password: str, driver: str, driverpath: str) -> None:
        self.user = user
        self.password = password
        self.driver = self.init_browser(driver, driverpath)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self) -> None:
        self.driver.get(self.INSTAGRAM_URL + 'accounts/login')
        sleep(2)

        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')

        username_field.send_keys(self.user)
        sleep(2)
        password_field.send_keys(self.password)
        sleep(2)
        password_field.send_keys(Keys.ENTER)

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')))
        except TimeoutException:
            raise exceptions.InvalidCredentials('Invalid credentials, not logged in')

    def deny_notifications(self) -> None:
        sleep(5)

        try:
            not_now_button = self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]')
        except NoSuchElementException:
            try:
                not_now_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]')
            except NoSuchElementException:
                return
        
        not_now_button.click()
    
    def comment_post(self, post_element: webelement, comment: str) -> None:
        form = post_element.find_element_by_tag_name('form')
        textarea = form.find_element_by_tag_name('textarea')
        button = form.find_element_by_tag_name('button')

        try:
            textarea.click()
            textarea.send_keys(comment)

            sleep(1)

            button.click()
        except ElementNotInteractableException:
            pass

    def like_posts_by_hashtag(self, hashtag: str, quantity=100, comment='') -> int:
        liked_posts = 0
        
        self.driver.get(self.INSTAGRAM_URL + f'explore/tags/{hashtag}')
        sleep(5)

        self.driver.find_element_by_class_name('_9AhH0').click()
        
        while liked_posts < quantity:
            sleep(2)

            try:
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fr66n > button:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)')))
                like_button = self.driver.find_element_by_css_selector('.fr66n > button:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)')

                if not like_button.get_attribute('fill') == '#ed4956':
                    like_button.click()
                    liked_posts += 1

                    if comment:
                        try:
                            sleep(randint(1, 2))

                            article = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article')
                            form = article.find_element_by_tag_name('form')
                            textarea = form.find_element_by_tag_name('textarea')

                            textarea.click()

                            self.comment_post(article, comment)

                            sleep(randint(1, 3))
                        except NoSuchElementException:
                            pass
                    
                self.driver.find_element_by_class_name('_65Bje').click()
            except (ElementClickInterceptedException, NoSuchElementException, TimeoutException):
                return liked_posts

            sleep(randint(5, 15))
        
        return liked_posts

    def like_feed_posts(self, quantity=100, comment='') -> int:
        self.driver.get(self.INSTAGRAM_URL)
        self.deny_notifications()
        navbar = self.driver.find_element_by_xpath('/html/body/div[1]/section/nav')
        self.driver.execute_script('arguments[0].remove();', navbar)

        liked_posts = 0

        while liked_posts < quantity:
            articles = self.driver.find_elements_by_css_selector('article._8Rm4L')
            
            try:
                for article in articles:
                    svg = article.find_element_by_css_selector('div:nth-child(4) > section:nth-child(1) > span:nth-child(1) > button:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)')

                    if not svg.get_attribute('fill') == '#ed4956':
                        try:
                            svg.click()
                            liked_posts += 1

                            if comment:
                                sleep(randint(1, 2))

                                form = article.find_element_by_tag_name('form')
                                textarea = form.find_element_by_tag_name('textarea')

                                textarea.click()

                                self.comment_post(article, comment)

                                sleep(randint(1, 3))
                        except ElementClickInterceptedException:
                            try:
                                self.driver.execute_script('arguments[0].scrollIntoView();', svg)
                                svg.click()
                                liked_posts += 1
                            except ElementClickInterceptedException:
                                pass
                    else:
                        self.driver.execute_script('window.scrollBy(0, window.innerHeight / 2);')
                
                    sleep(randint(1, 4))
            except (StaleElementReferenceException, NoSuchElementException):
                self.driver.execute_script('window.scrollBy(0, window.innerHeight / 2);')
                continue

        return liked_posts
        
    def follow_suggested(self, quantity=100, ignore: List[str] = []) -> int:
        followed = 0
        counter = 1

        self.driver.get(self.INSTAGRAM_URL + 'explore/people/suggested/')
        sleep(5)

        while followed < quantity:
            try:
                user = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/div/div/div[' + str(counter) + ']/div[2]/div[1]/div/span')

                if user.text not in ignore:
                    follow_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/div/div/div[' + str(counter) + ']/div[3]/button')
                    follow_button.click()

                    followed += 1
            except NoSuchElementException:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].scrollIntoView();', follow_button)
                sleep(5)
                follow_button.click()

                followed += 1
            
            counter += 1
            sleep(randint(5, 12))
        
        return followed

    def unfollow(self, quantity=100, ignore: List[str]=[], all=False) -> None:
        unfollowed = 0
        following_users = [user for user in self.get_following(self.user, quantity, all)]

        for user in following_users:
            if user not in ignore:
                try:
                    self.driver.get(self.INSTAGRAM_URL + user)
                    self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_5f5mN')))

                    self.driver.find_element_by_class_name('_5f5mN').click()
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')))

                    self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                    unfollowed += 1
                    sleep(randint(2, 7))
                except TimeoutException:
                    return unfollowed
            
        return unfollowed

    def search_follower(self, search_account: str, account: str) -> bool:
        for follower in self.get_followers(search_account, all=True):
            if follower == account:
                return True
        
        return False

    def search_following(self, search_account: str, account: str) -> bool:
        for following in self.get_following(search_account, all=True):
            if following == account:
                return True
        
        return False

    def search_not_followers(self) -> Iterable[str]:
        followers = [follower for follower in self.get_followers(self.user, all=True)]
        following = [following for following in self.get_following(self.user, all=True)]

        not_followers = [user for user in following if user not in followers]

        return not_followers

    def unfollow_not_followers(self, ignore: List[str] = []) -> int:
        unfollowed = 0
        not_followers = [user for user in self.search_not_followers() if user not in ignore]

        for not_follower in not_followers:
            try:
                self.driver.get(self.INSTAGRAM_URL + not_follower)
                self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_5f5mN')))

                self.driver.find_element_by_class_name('_5f5mN').click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')))

                self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                unfollowed += 1
                sleep(randint(2, 7))
            except TimeoutException:
                return unfollowed
        
        return unfollowed

    def get_followers(self, account: str, quantity=100, all=False) -> Iterator[str]:
        self.driver.get(self.INSTAGRAM_URL + account)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/" + account +"/followers/']")))
        
        followers_button = self.driver.find_element_by_css_selector("a[href*='/" + account +"/followers/']")

        if all:
            quantity = int(followers_button.text.split()[0])

        followers_button.click()

        try:
            xpath = '/html/body/div[4]/div/div/div[2]/ul/div/li['
            self.driver.find_element_by_xpath(xpath + '1]')
        except NoSuchElementException:
            xpath = '/html/body/div[5]/div/div/div[2]/ul/div/li['

        for i in range(1, quantity + 1):
            try:
                follower_li = self.driver.find_element_by_xpath(xpath + f'{i}]')
            except NoSuchElementException:
                try:
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath + f'{i}]')))
                    follower_li = self.driver.find_element_by_xpath(xpath + f'{i}]')
                except TimeoutException:
                    break
            
            follower = follower_li.text.split()[0]
            self.driver.execute_script('arguments[0].scrollIntoView();', follower_li)
            sleep(0.5)

            yield follower

    def get_following(self, account: str, quantity=100, all=False) -> Iterator[str]:
        self.driver.get(self.INSTAGRAM_URL + account)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/" + account +"/following/']")))

        following_button = self.driver.find_element_by_css_selector("a[href*='/" + account +"/following/']")

        if all:
            quantity = int(following_button.text.split()[0])

        following_button.click()

        try:
            xpath = '/html/body/div[4]/div/div/div[2]/ul/div/li['
            self.driver.find_element_by_xpath(xpath + '1]')
        except NoSuchElementException:
            xpath = '/html/body/div[5]/div/div/div[2]/ul/div/li['

        for i in range(1, quantity + 1):
            try:
                following_li = self.driver.find_element_by_xpath(xpath + f'{i}]')
            except NoSuchElementException:
                try:
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath + f'{i}]')))
                    following_li = self.driver.find_element_by_xpath(xpath + f'{i}]')
                except TimeoutException:
                    break
            
            following = following_li.text.split()[0]
            self.driver.execute_script('arguments[0].scrollIntoView();', following_li)
            sleep(0.5)

            yield following

    def close_browser(self):
        self.driver.quit()

    def init_browser(self, driver: str, driverpath: str) -> WebDriver:
        if driver == 'chrome':
            driver_model = webdriver.Chrome
        elif driver == 'firefox':
            driver_model = webdriver.Firefox
        elif driver == 'safari':
            driver_model = webdriver.Safari
        else:
            driver_model = None

        try:
            browser = driver_model(executable_path=driverpath, service_log_path=devnull, log_path=devnull)
        except TypeError:
            raise exceptions.InvalidDriverModel('This driver model is not supported')
        except WebDriverException:
            raise exceptions.InvalidDriverPath('Driver executable needs to be in PATH')

        return browser
