import pytest


@pytest.mark.parametrize('code', ['P00006BXP0000', 'P00006BXP12KW'])
def test_selenium_verify_url(
    code, processes_scraping_factory, process_number_tjal, url_tjal_2g
):
    scraping = processes_scraping_factory(url_tjal_2g, process_number_tjal)

    new_urls = scraping.verify_url(url_tjal_2g)

    assert (
        f'https://www2.tjal.jus.br/cposg5/show.do?processo.codigo={code}'
        in new_urls
    )


def test_selenium_get_basic_data(
    processes_scraping_factory, process_number_tjal, url_tjal_1g
):
    scraping = processes_scraping_factory(url_tjal_1g, process_number_tjal)

    result = scraping.get_basic_data([])

    assert result is None


def test_selenium_get_process_parties(
    processes_scraping_factory, process_number_tjal, url_tjal_1g
):
    scraping = processes_scraping_factory(url_tjal_1g, process_number_tjal)

    result = scraping.get_process_parties()

    assert result == {
        'authors': [
            'José Carlos Cerqueira Souza Filho',
            'Advogado:  Vinicius Faria de Cerqueira',
            'Livia Nascimento da Rocha',
            'Advogado:  Vinicius Faria de Cerqueira',
        ],
        'defendants': [
            'Cony Engenharia Ltda.',
            'Advogado: Carlos Henrique de Mendonça Brandão',
            'Advogado: Guilherme Freire Furtado',
            'Advogada: Maria Eugênia Barreiros de Mello',
            'Advogado: Vítor Reis de Araujo Carvalho',
            'Banco do Brasil S A',
            'Advogado: Nelson Wilians Fratoni Rodrigues',
        ],
    }


def test_selenium_get_movimentations(
    processes_scraping_factory, process_number_tjal, url_tjal_1g
):
    scraping = processes_scraping_factory(url_tjal_1g, process_number_tjal)

    result = scraping.get_movimentations()

    assert len(result) > 1
    assert result[0] == {
        'date': '22/02/2021',
        'description': 'Remetido recurso eletrônico'
        + ' ao Tribunal de Justiça/Turma de recurso',
    }


@pytest.mark.parametrize(
    'process_number,expected',
    [
        (
            '07108025520188020001',
            {
                'process_number': '07108025520188020001',
                'class': 'Procedimento Comum Cível',
                'area': 'Cível',
                'topic': 'Dano Material',
                'distribution_date': '2018-05-02 19:01',
                'judge': 'José Cícero Alves da Silva',
                'stock_price': 'R$ 281.178,42',
                'degree': '1º Grau',
                'state': 'TJAL',
            },
        ),
        (
            '00703379120088060001',
            {
                'process_number': '00703379120088060001',
                'class': 'Ação Penal - Procedimento Ordinário',
                'area': 'Criminal',
                'topic': 'Crimes de Trânsito',
                'distribution_date': '2018-05-02 09:13',
                'judge': None,
                'stock_price': None,
                'degree': '1º Grau',
                'state': 'TJCE',
            },
        ),
    ],
)
def test_selenium_run_processes(process_number, expected):
    from core.scrapper.selenium.app import ProcessesScraping

    scraping = ProcessesScraping()

    payload = scraping.run(process_number)

    del payload[0]['process_parties']
    del payload[0]['movimentations']

    assert isinstance(payload, list)
    assert payload[0] == expected
