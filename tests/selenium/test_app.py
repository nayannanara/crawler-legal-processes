import pytest


@pytest.mark.parametrize('code', ['P00006BXP0000', 'P00006BXP12KW'])
def test_verify_url(
    code, processes_scraping_factory, process_number_tjal, url_tjal_2g
):
    scraping = processes_scraping_factory(url_tjal_2g, process_number_tjal)

    new_urls = scraping.verify_url(url_tjal_2g)

    assert (
        f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={code}'
        in new_urls
    )


def test_initial_process(
    processes_scraping_factory, process_number_tjal, url_tjal_1g
):
    key_name = '1º Grau - TJAL'
    scraping = processes_scraping_factory(url_tjal_1g, process_number_tjal)

    payload = scraping.initial_process({})

    assert isinstance(payload, dict)
    assert process_number_tjal in payload.keys()
    assert key_name in payload[process_number_tjal].keys()


def test_get_basic_data(
    processes_scraping_factory, process_number_tjal, url_tjal_1g
):
    scraping = processes_scraping_factory(url_tjal_1g, process_number_tjal)

    payload = scraping.get_basic_data()

    del payload['process_parties']
    del payload['movimentations']

    assert isinstance(payload, dict)
    assert payload == {
        'process_number': '07108025520188020001',
        'class': 'Procedimento Comum Cível',
        'area': 'Cível',
        'topic': 'Dano Material',
        'distribution_date': '02/05/2018 19:01',
        'judge': 'José Cícero Alves da Silva',
        'stock_price': 'R$ 281.178,42',
    }


def test_run_processes(process_number_tjal, process_number_tjce):
    from core.scrapper.selenium.app import ProcessesScraping
    from utils.driver_selenium import selenium_driver

    driver = selenium_driver.driver
    scraping = ProcessesScraping(driver)

    key_name = '1º Grau - TJCE'

    payload = scraping.run(f'{process_number_tjal}, {process_number_tjce}')

    assert isinstance(payload, dict)
    assert key_name in payload[process_number_tjce].keys()
    assert payload[process_number_tjce][key_name][0]['process_parties'] == {
        'authors': ['Ministério Público do Estado do Ceará'],
        'defendants': [
            'G. de O. C.',
            'A. S. F.',
            'Departamento de Tecnologia da Informação e Comunicação - DETIC (Polícia Civil)',
            'M. L. S. I.',
        ],
    }
    assert payload[process_number_tjce][key_name][0]['movimentations']
    assert (
        len(
            payload[process_number_tjce]['1º Grau - TJCE'][0]['movimentations']
        )
        > 1
    )
