import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from src.models.driver import Driver

class Scraper:
    def __init__(self, root_url, target_meal):
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)
        self.__root_url = root_url
        self.__target_meal = target_meal
        self.__driver = Driver()

    @property
    def credentials(self):
        username = os.getenv('USER')
        password = os.getenv('PASS')
        if username and password:
            return {
                'username': username,
                'password': password
            }
        else:
            raise Exception('Credentials not found!')

    def __wait(self, condition, timeout=30):
        WebDriverWait(
            self.browser,
            timeout=timeout
        ).until(
            condition
        )

    def set_log_prefix(self, msg):
        self.__prefix = f'{msg} - '

    def __log(self, msg):
        prefix = self.__prefix if self.__prefix else ''
        logging.info(prefix + msg)

    def __click_btn(self, btn_name='submit'):
        self.browser.find_element(By.NAME, btn_name).send_keys("webdriver" + Keys.ENTER)

    def __click_link(self, text):
        self.browser.find_element(By.LINK_TEXT, text).send_keys("webdriver" + Keys.ENTER)

    def reserve(self):
        self.set_log_prefix('[ RESERVATION ]')

        self.__log('Making Reservation')
        self.__click_link('Agendar refeição')
        self.__log('.')

        select_element = self.browser.find_element(By.ID,'agendamentoForm:refeicao')
        select_object = Select(select_element)
        self.__log('..')
        select_object.select_by_visible_text(self.__target_meal)
        self.__log('...')

        self.__click_btn('agendamentoForm:j_idt93')
        self.__log('Succeeded!')

    def login(self):
        self.set_log_prefix('[ LOGIN ]')

        self.browser.get(self.__root_url)
        self.__log(f'Authenticating')

        # Wait For Redirect
        wait_condition = lambda driver: driver.find_element_by_id('logintxt')
        self.__wait(wait_condition)
        self.__log('.')

        # Authenticate
        username = self.browser.find_element_by_id("username")
        username.send_keys(self.credentials.get("username"))
        self.__log('..')
        password = self.browser.find_element_by_id("password")
        password.send_keys(self.credentials.get("password"))
        self.__log('...')

        self.__click_btn()
        self.__log('Succeeded!')

    def make_reservation(self, save_img=False):
        self.browser = self.__driver.browser

        self.set_log_prefix('[ INFO ]')
        self.__log(f'Page: {self.__root_url}')
        self.__log(f'Meal: {self.__target_meal}')
        self.__log(f'User: {self.credentials.get("username")}')

        self.login()
        self.reserve()
        if save_img:
            self.browser.save_screenshot('reservation.png')
