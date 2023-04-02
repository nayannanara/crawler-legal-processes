import asyncio
from typing import AsyncGenerator, Callable, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_mock import MockerFixture
from selenium.webdriver.common.by import By
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.configs.database import async_session, engine
from core.configs.deps import get_session
from core.contrib.models import BaseModel
from core.processes.schemas import ProcessIn
from core.processes.usecases import ProcessUseCase
from core.scrapper.selenium.app import ProcessesScraping
from tests.factories import minimal_process_out_tjal, minimal_process_out_tjce
from utils.driver_selenium import selenium_driver

from .fixture_package.routers import routers as fixture_routers


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)

        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture
def database(db_session: AsyncSession) -> Callable:
    async def _database():
        yield db_session

    return _database


@pytest.fixture
def app(database: Callable) -> FastAPI:
    from core.main import app

    app.dependency_overrides[get_session] = database

    return app


@pytest.mark.anyio
@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url='http://processes') as ac:
        yield ac


@pytest.fixture
def routers():
    return fixture_routers


@pytest.fixture
def payload() -> dict:
    return [
        {
            'process_number': '07108025520188020001',
            'class': 'Procedimento Comum Cível',
            'area': 'Cível',
            'topic': 'Dano Material',
            'distribution_date': '2018-05-02 19:01',
            'judge': 'José Cícero Alves da Silva',
            'stock_price': 'R$ 281.178,42',
            'degree': '1º Grau',
            'state': 'TJCE',
            'process_parties': {
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
            },
            'movimentations': [
                {
                    'date': '22/02/2021',
                    'description': 'Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso',
                }
            ],
        }
    ]


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


@pytest.fixture
def process_usecase():
    return ProcessUseCase()


@pytest.fixture
def get_url(process_number_tjal):
    return f'api/v0/processes/{process_number_tjal}'


@pytest.fixture
def post_url():
    return 'api/v0/processes/'


@pytest.fixture
def query_url():
    return 'api/v0/processes/'


@pytest.fixture
def process_in(process_number_tjal):
    return ProcessIn(process_number=process_number_tjal)


@pytest.fixture
async def create_processes(
    process_usecase, process_in, db_session, mock_scraping_run
):
    mock_scraping_run.return_value = minimal_process_out_tjal()
    return await process_usecase.create(process_in, db_session)


@pytest.fixture
async def mock_scraping_run(mocker: MockerFixture):
    return mocker.patch.object(
        ProcessesScraping, 'run', return_value=minimal_process_out_tjce()
    )


@pytest.fixture
def teste():
    [
        {
            'process_number': '07108025520188020001',
            'class': 'Procedimento Comum Cível',
            'area': 'Cível',
            'topic': 'Dano Material',
            'distribution_date': '2018-05-02T19:01:00',
            'judge': 'José Cícero Alves da Silva',
            'stock_price': 'R$ 281.178,42',
            'process_parties': {
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
            },
            'degree': '1º Grau',
            'state': 'TJAL',
            'movimentations': [
                {
                    'date': '22/02/2021',
                    'description': 'Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso',
                },
                {
                    'date': '10/02/2021',
                    'description': 'Juntada de Documento\nNº Protocolo: WMAC.21.70031538-2 Tipo da Petição: Contrarrazões Data: 10/02/2021 19:27',
                },
                {
                    'date': '06/01/2021',
                    'description': 'Ato Publicado\nRelação :0003/2021 Data da Publicação: 21/01/2021 Número do Diário: 2738',
                },
                {
                    'date': '06/01/2021',
                    'description': 'Ato Publicado\nRelação :0003/2021 Data da Publicação: 21/01/2021 Número do Diário: 2738',
                },
                {
                    'date': '06/01/2021',
                    'description': 'Ato Publicado\nRelação :0003/2021 Data da Publicação: 21/01/2021 Número do Diário: 2738',
                },
            ],
            'created_at': '2023-04-02T11:05:02.247909',
        }
    ]
