import pytest
from fastapi import status

from core.processes.schemas import ProcessOut


@pytest.mark.asyncio
async def test_integration_get_processes_should_return_success(client, get_url, create_processes):
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

#f'{process_number_tjce},{process_number_tjal}'}
@pytest.mark.asyncio
async def test_integration_post_processes_should_return_success(
    client, post_url, process_number_tjce, process_number_tjal
):
    response = await client.post(
        post_url, json={'process_number': process_number_tjce}
    )

    content = response.json()

    process_out = ProcessOut.parse_obj(content[0])

    del content[0]['created_at']
    del content[0]['distribution_date']

    assert response.status_code == status.HTTP_201_CREATED
    assert content[0] == process_out.dict(
        by_alias=True, exclude={'distribution_date', 'created_at'}
    )


@pytest.mark.asyncio
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
