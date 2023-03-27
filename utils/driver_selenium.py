from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumWebDriver:
    def __init__(self) -> None:
        logger.info(f'Iniciando Scraping')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        logger.info('Iniciando Chrome')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            chrome_options=chrome_options,
        )

        logger.info('Chrome iniciado com sucesso')


selenium_driver = SeleniumWebDriver()
