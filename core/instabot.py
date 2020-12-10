from selenium import webdriver
from os import devnull
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random import randint
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException, TimeoutException
from . import exceptions
from time import sleep
from typing import Iterator, Iterable, List

class Bot:
    INSTAGRAM_URL: str = 'https://www.instagram.com/'

    def __init__(self, usuario: str, senha: str, driver: str, driverpath: str) -> None:
        self.usuario = usuario
        self.senha = senha
        self.driver = self.init_browser(driver, driverpath)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self) -> None:
        self.driver.get(self.INSTAGRAM_URL + 'accounts/login')
        sleep(2)

        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')

        username_field.send_keys(self.usuario)
        sleep(2)
        password_field.send_keys(self.senha)
        sleep(2)
        password_field.send_keys(Keys.ENTER)

        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span')))
        except TimeoutException:
            raise exceptions.InvalidCredentials('Invalid credentials, not logged in. Aborting.')

    def like_photos_by_hashtag(self, hashtag: str, quantity=100) -> int:
        liked_photos = 0
        
        self.driver.get(self.INSTAGRAM_URL + f'explore/tags/{hashtag}')
        sleep(5)

        self.driver.find_element_by_class_name('_9AhH0').click()
        
        while liked_photos < quantity:
            sleep(2)

            try:
                self.driver.find_element_by_class_name('fr66n').click()
                liked_photos += 1
                self.driver.find_element_by_class_name('_65Bje').click()
            except (ElementClickInterceptedException, NoSuchElementException):
                return liked_photos

            sleep(randint(5, 15))
        
        return liked_photos

    def follow_suggested(self, quantity=100, ignore: List[str] = []) -> int:
        followed = 0

        self.driver.get(self.INSTAGRAM_URL + 'explore/people/suggested/')
        sleep(5)

        while followed < quantity:
            try:
                follow_button = self.driver.find_element_by_xpath('//button[text()="Seguir"]')
                follow_button.click()
                followed += 1
            except NoSuchElementException:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except ElementClickInterceptedException:
                self.driver.execute_script('arguments[0].scrollIntoView();', follow_button)
                sleep(5)
                follow_button.click()
                
            sleep(randint(5, 10))
        
        return followed

    def unfollow(self, quantity=100, ignore: List[str]=[], all=False) -> None:
        following_users = [user for user in self.get_following(self.usuario, quantity, all)]

        for user in following_users:
            if user not in ignore:
                self.driver.get(self.INSTAGRAM_URL + user)
                self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '5f5mN')))

                self.driver.find_element_by_class_name('_5f5mN').click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')))

                self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
                sleep(randint(2, 7))

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
        followers = [follower for follower in self.get_followers(self.usuario, all=True)]
        following = [following for following in self.get_following(self.usuario, all=True)]

        not_followers = [user for user in following if user not in followers]

        return not_followers

    def unfollow_not_followers(self, ignore: List[str] = []) -> None:
        not_followers = [user for user in self.search_not_followers() if user not in ignore]

        for not_follower in not_followers:
            self.driver.get(self.INSTAGRAM_URL + not_follower)
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_5f5mN')))

            self.driver.find_element_by_class_name('_5f5mN').click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[1]')))

            self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[1]').click()
            sleep(randint(2, 7))

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
        self.driver.close()

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
