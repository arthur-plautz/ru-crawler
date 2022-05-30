import logging
import os
from time import sleep
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

    def __select_hour(self, select_object):
        best_hour = {
            'Almoço': 4,
            'Jantar': 3
        }
        target_hour = best_hour[self.__target_meal]
        while target_hour > 0:
            try:
                select_object.select_by_index(target_hour)
                self.__log(f'(Hour Selection) Option number {target_hour} selected.')
                return True
            except:
                self.__log(f'(Hour Selection) Option number {target_hour} not found, changing parameters...')
                target_hour -= 1
        else:
            raise Exception("(Hour Selection) No option found.")

    def reserve(self):
        self.set_log_prefix('[ RESERVATION ]')

        self.__log('Making Reservation')
        self.__click_link('Agendar refeição')
        self.__log('.')

        select_meal_element = self.browser.find_element_by_name('agendamentoForm:refeicao')
        select_meal_object = Select(select_meal_element)
        select_meal_object.select_by_visible_text(self.__target_meal)

        sleep(1)
        self.__log('..')

        select_date_element = self.browser.find_element_by_name("agendamentoForm:dtRefeicao")
        select_date_object = Select(select_date_element)
        select_date_object.select_by_index(1)

        sleep(1)
        self.__log('...')

        select_hour_element = self.browser.find_element_by_name("agendamentoForm:hrRefeicao")
        select_hour_object = Select(select_hour_element)
        self.__select_hour(select_hour_object)

        sleep(1)
        self.__log('....')

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
