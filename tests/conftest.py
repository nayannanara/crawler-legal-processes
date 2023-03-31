import pytest
from selenium.webdriver.common.by import By

from core.scrapper.selenium.app import ProcessesScraping
from utils.driver_selenium import selenium_driver


@pytest.fixture
def scraping():
    return ProcessesScraping()


@pytest.fixture
def process_number_tjal() -> str:
    return '07108025520188020001'


@pytest.fixture
def process_number_tjce() -> str:
    return '00703379120088060001'


@pytest.fixture
def url_tjal_1g() -> str:
    return 'https://www2.tjal.jus.br/cpopg/open.do'


@pytest.fixture
def url_tjal_2g() -> str:
    return 'https://www2.tjal.jus.br/cposg5/open.do'


@pytest.fixture
def url_tjce_1g() -> str:
    return 'https://esaj.tjce.jus.br/cpopg/open.do'


@pytest.fixture
def url_tjce_2g() -> str:
    return 'https://esaj.tjce.jus.br/cposg5/open.do'


@pytest.fixture
def processes_scraping_factory():
    def _factory(url, process_number):
        driver = selenium_driver.driver
        scraping = ProcessesScraping()
        scraping.process_number = process_number

        driver.get(url)
        driver.find_element(By.NAME, 'numeroDigitoAnoUnificado').send_keys(
            process_number[0:13]
        )

        input_forum = driver.find_element(By.NAME, 'foroNumeroUnificado')
        input_forum.send_keys(process_number[-4:])
        input_forum.submit()

        return scraping

    return _factory
