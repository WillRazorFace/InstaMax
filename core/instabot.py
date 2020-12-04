from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from random import randint
from selenium.common.exceptions import WebDriverException, NoSuchElementException, ElementClickInterceptedException
import exceptions
from time import sleep

class Bot:
    def __init__(self, usuario: str, senha: str, driver: str, driverpath: str) -> None:
        self.usuario = usuario
        self.senha = senha
        self.driver = self.init_browser(driver, driverpath)

    def login(self) -> None:
        self.driver.get('https://www.instagram.com/accounts/login')
        sleep(2)

        username_field = self.driver.find_element_by_name('username')
        password_field = self.driver.find_element_by_name('password')

        username_field.send_keys(self.usuario)
        sleep(2)
        password_field.send_keys(self.senha)
        sleep(2)
        password_field.send_keys(Keys.ENTER)
        sleep(5)

    def like_photos_by_hashtag(self, hashtag: str, quantity=60) -> int:
        liked_photos = 0
        
        self.driver.get(f'https://www.instagram.com/explore/tags/{hashtag}')
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

            sleep(randint(5, 25))
        
        return liked_photos

    def close_browser(self):
        self.driver.close()

    def init_browser(self, driver: str, driverpath: str) -> WebDriver:
        if driver == 'chrome':
            driver_model = webdriver.Chrome
        elif driver == 'firefox':
            driver_model = webdriver.Firefox
        elif driver == 'edge':
            driver_model = webdriver.Edge
        elif driver == 'safari':
            driver_model = webdriver.Safari
        else:
            driver_model = None

        try:
            browser = driver_model(driverpath)
        except TypeError:
            raise exceptions.InvalidDriverModel('This driver model is not supported')
        except WebDriverException:
            raise exceptions.InvalidDriverPath('Driver executable needs to be in PATH')

        return browser

if __name__ == '__main__':
    insta_bot = Bot('associacaopadreguido', 'mtzika99', 'edge', 'msedgedriver.exe')
    insta_bot.login()
    print(insta_bot.like_photos_by_hashtag('catolicos', 100))
