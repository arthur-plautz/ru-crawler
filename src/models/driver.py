import os 
from selenium import webdriver

class Driver:
    def __init__(self):
        self.__build_path()
        self.build_options()
        self.build_browser()

    @property
    def path(self):
        return self.__path

    @property
    def browser(self):
        return self.__browser

    @property
    def options(self):
        return self.__options

    def __build_path(self):
        driver = os.getenv('DRIVER')
        if driver:
            drivers_path = '/usr/local/bin/'
            self.__path = drivers_path + driver
        else:
            raise Exception('Driver not defined!')

    def build_options(
        self,
        default_options=[
            '--headless',
            'start-maximized',
            'disable-infobars',
            '--disable-extensions',
            '--disable-dev-shm-usage',
            '--no-sandbox'
        ],
        additional_options=[]
    ):
        options = default_options + additional_options
        driver_options = webdriver.ChromeOptions()
        for option in options:
            driver_options.add_argument(option)
        self.__options = driver_options

    def build_browser(self):
        self.__browser = webdriver.Chrome(
            self.path,
            options=self.options
        )
