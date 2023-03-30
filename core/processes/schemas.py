from datetime import datetime

from pydantic import Field

from core.contrib.schemas import BaseSchemaMixin


class Movimentation(BaseSchemaMixin):
    date: str = Field(title='Movimentation date', example='22/02/2021')
    description: str = Field(
        ...,
        title='Movimentation description',
        example='Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso',
    )


class Process(BaseSchemaMixin):
    process_number: str = Field(
        ..., title='Process number', example='07108025520188020001'
    )
    class_: str = Field(
        alias='class',
        title='Process class',
        example='Procedimento Comum Cível',
    )
    area: str = Field(title='Process area', example='Cível')
    topic: str = Field(title='Process topic', example='Dano Material')
    distribution_date: datetime = Field(
        title='Date of distribution of process', example='02/05/2018 19:01'
    )
    judge: str = Field(
        title='Process judge', example='José Cícero Alves da Silva'
    )
    stock_price: str = Field(title='Stock price', example='281.178,42')
    process_parties: dict[str, list[str]] = Field(
        title='Process parties',
        example={
            'authors': ['José Carlos Cerqueira Souza Filho'],
            'defendants': ['Cony Engenharia Ltda.'],
        },
    )
    degree: str = Field(title='Process degree', example='1º Grau')
    state: str = Field(title='Process state', example='TJAL')
    movimentations: list[Movimentation] = Field(
        title='Process movimentations',
        example=[
            {
                'date': '22/02/2021',
                'description': 'Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso',
            }
        ],
    )


class ProcessOut(Process):
    id: int
    created_at: datetime = Field(title='Creation date')


class ProcessIn(BaseSchemaMixin):
    process_number: str = Field(
        ..., title='Process number', example='07108025520188020001'
    )
