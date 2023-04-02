from unittest import mock

import pytest
import sqlalchemy
from fastapi import status

from core.processes.schemas import ProcessOut


@pytest.mark.usefixtures('create_processes')
async def test_integration_get_processes_should_return_success(
    client, get_url
):
    response = await client.get(get_url)

    content = response.json()

    del content['movimentations']
    del content['created_at']

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        'process_number': '07108025520188020001',
        'class': None,
        'area': 'Cível',
        'topic': 'Obrigações',
        'distribution_date': None,
        'judge': None,
        'stock_price': None,
        'process_parties': {
            'authors': [
                'Cony Engenharia Ltda.',
                'Advogado:  Carlos Henrique de Mendonça Brandão',
                'Advogada:  Maria Eugênia Barreiros de Mello',
                'Advogado:  Guilherme Freire Furtado',
                'Advogado:  Vítor Reis de Araujo Carvalho',
            ],
            'defendants': [
                'José Carlos Cerqueira Souza Filho',
                'Advogado: Vinicius Faria de Cerqueira',
                'Livia Nascimento da Rocha',
                'Advogado: Vinicius Faria de Cerqueira',
                'Banco do Brasil S A',
                'Advogado: Nelson Wilians Fratoni Rodrigues',
                'Advogado: Louise Rainer Pereira Gionédis',
                'Advogado: Louise Rainer Pereira Gionédis',
            ],
        },
        'degree': '2º Grau',
        'state': 'TJAL',
    }


async def test_integration_get_processes_should_not_found(client, get_url):
    response = await client.get(get_url)

    content = response.json()

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert content == {
        'detail': 'Process not found for number: 07108025520188020001'
    }


async def test_integration_post_processes_should_return_success(
    client, post_url, process_number_tjal
):
    response = await client.post(
        post_url, json={'process_number': process_number_tjal}
    )

    content = response.json()

    process_out = ProcessOut.parse_obj(content[0])

    del content[0]['created_at']
    del content[0]['distribution_date']

    assert response.status_code == status.HTTP_201_CREATED
    assert content[0] == process_out.dict(
        by_alias=True, exclude={'distribution_date', 'created_at'}
    )


@mock.patch('sqlalchemy.ext.asyncio.AsyncSession.commit')
async def test_integration_post_processes_should_return_internal_server_error(
    mock_commit, client, post_url, process_number_tjal
):
    mock_commit.side_effect = sqlalchemy.exc.IntegrityError(
        mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
    )

    response = await client.post(
        post_url, json={'process_number': process_number_tjal}
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        'detail': 'Ocorreu um erro ao inserir o dado no banco de dados.'
    }


async def test_integration_post_processes_with_more_than_one_process_should_return_success(  # noqa
    client, post_url, process_number_tjce, process_number_tjal
):
    response = await client.post(
        post_url,
        json={
            'process_number': f'{process_number_tjce},{process_number_tjal}'
        },
    )

    content = response.json()

    process_out = ProcessOut.parse_obj(content[0])

    del content[0]['created_at']
    del content[0]['distribution_date']

    assert (process_number_tjce or process_number_tjal) in [
        i['process_number'] for i in content
    ]

    assert response.status_code == status.HTTP_201_CREATED
    assert content[0] == process_out.dict(
        by_alias=True, exclude={'distribution_date', 'created_at'}
    )


async def test_integration_post_processes_with_return_unprocessable_entity(
    client, post_url
):
    response = await client.post(
        post_url, json={'process_number': '12344479120088060001'}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': 'Processo(s) não encontrado(s)'}


async def test_integration_query_processes_should_return_success(
    client, query_url, create_processes
):
    response = await client.get(query_url)

    content = response.json()

    del content[0]['process_parties']
    del content[0]['movimentations']
    del content[0]['created_at']

    assert response.status_code == status.HTTP_200_OK
    assert len(content) > 1
    assert content[0]['process_number'] == create_processes[0].process_number
    assert content[0] == {
        'process_number': '07108025520188020001',
        'class': 'Procedimento Comum Cível',
        'area': 'Cível',
        'topic': 'Dano Material',
        'distribution_date': '2018-05-02T19:01:00',
        'judge': 'José Cícero Alves da Silva',
        'stock_price': 'R$ 281.178,42',
        'degree': '1º Grau',
        'state': 'TJAL',
    }


async def test_integration_query_processes_should_empty_list(
    client, query_url
):
    response = await client.get(query_url)

    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert content == []
