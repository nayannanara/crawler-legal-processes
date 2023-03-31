from time import sleep
from typing import Any

from loguru import logger
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.driver_selenium import selenium_driver
from utils.helpers import format_date
from utils.urls import URLS


class ProcessesScraping:
    driver: WebDriver = selenium_driver.driver

    def __init__(self: 'ProcessesScraping') -> None:
        self.process_number: str = ''

    def run(self: 'ProcessesScraping', input: str) -> list[dict[str, str]]:
        processes = input.split(',')
        payload: list[dict[str, str]] = []

        for process in processes:
            self.process_number = process.strip()

            for url in URLS:
                is_exists_process = True
                self.driver.get(url)
                self.driver.find_element(
                    By.NAME, 'numeroDigitoAnoUnificado'
                ).send_keys(self.process_number[0:13])

                input_forum = self.driver.find_element(
                    By.NAME, 'foroNumeroUnificado'
                )
                input_forum.send_keys(self.process_number[-4:])
                input_forum.submit()

                try:
                    self.driver.find_element(By.ID, 'mensagemRetorno')
                    is_exists_process = False
                except NoSuchElementException:
                    ...

                if not is_exists_process:
                    continue

                new_urls = self.verify_url(url)

                if not len(new_urls) > 1:
                    self.get_basic_data(payload)
                else:
                    for url in new_urls:
                        self.driver.get(url)
                        self.get_basic_data(payload)

        return payload

    def verify_url(self: 'ProcessesScraping', url: str) -> list[str]:
        urls = [
            'https://www2.tjal.jus.br/cposg5/open.do',
            'https://esaj.tjce.jus.br/cposg5/open.do',
        ]
        new_urls = []

        if url in urls:
            sleep(2)
            modal = self.driver.find_element(
                By.CLASS_NAME, 'modal__lista-processos'
            )
            processes_list = modal.find_elements(By.CLASS_NAME, 'custom-radio')

            for process in processes_list:
                process_code = process.get_attribute('value')
                new_host = url.split('/open.do')[0]
                new_urls.append(
                    f'{new_host}/show.do?processo.codigo={process_code}'
                )

        return new_urls

    def get_basic_data(
        self: 'ProcessesScraping', payload: list[dict[str, str]]
    ) -> None:
        details = self.driver.find_element(By.ID, 'maisDetalhes')

        self.driver.execute_script(
            "arguments[0].setAttribute('class','collapse show')", details
        )
        degree = self.driver.find_element(By.TAG_NAME, 'h1').text[-7:]
        state = self.driver.find_element(
            By.CLASS_NAME, 'header__navbar__brand__initials'
        ).text

        try:
            class_ = self.driver.find_element(
                By.ID, 'classeProcesso'
            ).text.strip()
        except NoSuchElementException:
            class_ = None

        area = self.driver.find_element(By.ID, 'areaProcesso').text.strip()
        topic = self.driver.find_element(By.ID, 'assuntoProcesso').text.strip()
        try:
            distribution_date_str = self.driver.find_element(
                By.ID, 'dataHoraDistribuicaoProcesso'
            ).text.split('-')
            new_distribution_date = (
                distribution_date_str[0]
                .strip()
                .replace('às', '')
                .replace('  ', ' ')
                .strip()
            )
            distribution_date = format_date(new_distribution_date)
        except NoSuchElementException:
            distribution_date = None

        try:
            judge = self.driver.find_element(
                By.ID, 'juizProcesso'
            ).text.strip()
        except NoSuchElementException:
            judge = None

        try:
            stock_price = self.driver.find_element(
                By.ID, 'valorAcaoProcesso'
            ).text.strip()
        except NoSuchElementException:
            stock_price = None

        data = {
            'process_number': self.process_number,
            'class': class_,
            'area': area,
            'topic': topic,
            'distribution_date': distribution_date,
            'judge': judge,
            'stock_price': stock_price,
            'degree': degree,
            'state': state,
        }

        data.update(
            {
                'process_parties': self.get_process_parties(),  # type: ignore
                'movimentations': self.get_movimentations(),  # type: ignore
            }
        )
        payload.append(data)

    def get_process_parties(self: 'ProcessesScraping') -> dict[Any, Any]:
        try:
            process_parties_table = self.driver.find_element(
                By.ID, 'tableTodasPartes'
            )
        except NoSuchElementException:
            process_parties_table = self.driver.find_element(
                By.ID, 'tablePartesPrincipais'
            )

        self.driver.execute_script(
            "arguments[0].style.display = 'table';", process_parties_table
        )

        parties_trs = process_parties_table.find_elements(By.TAG_NAME, 'tr')

        authors: list[str] = []
        defendants: list[str] = []

        for tr in parties_trs:
            part = tr.find_element(By.CLASS_NAME, 'tipoDeParticipacao')

            if part.text.strip() in [
                'Autor',
                'Autora',
                'Apelante:',
                'Embargante:',
            ]:
                names = (
                    tr.find_element(By.CLASS_NAME, 'nomeParteEAdvogado')
                    .text.strip()
                    .replace('\n', ', ')
                )
                [
                    authors.append(name.strip())  # type: ignore
                    for name in names.split(',')
                ]
            else:
                names = (
                    tr.find_element(By.CLASS_NAME, 'nomeParteEAdvogado')
                    .text.strip()
                    .replace('\n', ', ')
                    .replace('  ', ' ')
                )
                [
                    defendants.append(name.strip())  # type: ignore
                    for name in names.split(',')
                ]
        data = {'authors': authors, 'defendants': defendants}

        return data

    def get_movimentations(self: 'ProcessesScraping') -> list[Any]:
        movimentations_table = self.driver.find_element(
            By.ID, 'tabelaTodasMovimentacoes'
        )
        self.driver.execute_script(
            "arguments[0].style.display = 'table';", movimentations_table
        )

        movimentations_trs = movimentations_table.find_elements(
            By.TAG_NAME, 'tr'
        )

        movimentations = []

        for movimentation in movimentations_trs:
            try:
                movimentation_date = movimentation.find_element(
                    By.CLASS_NAME, 'dataMovimentacao'
                ).text.strip()
            except NoSuchElementException:
                movimentation_date = movimentation.find_element(
                    By.CLASS_NAME, 'dataMovimentacaoProcesso'
                ).text.strip()
            try:
                movimentation_description = movimentation.find_element(
                    By.CLASS_NAME, 'descricaoMovimentacao'
                ).text.strip()
            except NoSuchElementException:
                movimentation_description = movimentation.find_element(
                    By.CLASS_NAME, 'descricaoMovimentacaoProcesso'
                ).text.strip()

            movimentations.append(
                {
                    'date': movimentation_date,
                    'description': movimentation_description,
                }
            )

        return movimentations
