from datetime import datetime
from typing import Optional

import orjson
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
    class_: Optional[str] = Field(
        nullable=True,
        alias='class',
        title='Process class',
        example='Procedimento Comum Cível',
    )
    area: Optional[str] = Field(
        nullable=True, title='Process area', example='Cível'
    )
    topic: Optional[str] = Field(
        nullable=True, title='Process topic', example='Dano Material'
    )
    distribution_date: Optional[datetime] = Field(
        nullable=True,
        title='Date of distribution of process',
        example='02/05/2018 19:01',
    )
    judge: Optional[str] = Field(
        nullable=True,
        title='Process judge',
        example='José Cícero Alves da Silva',
    )
    stock_price: Optional[str] = Field(
        nullable=True, title='Stock price', example='281.178,42'
    )
    process_parties: dict[str, list[str]] = Field(
        nullable=True,
        title='Process parties',
        example={
            'authors': ['José Carlos Cerqueira Souza Filho'],
            'defendants': ['Cony Engenharia Ltda.'],
        },
    )
    degree: Optional[str] = Field(
        nullable=True, title='Process degree', example='1º Grau'
    )
    state: Optional[str] = Field(
        nullable=True, title='Process state', example='TJAL'
    )
    movimentations: list[Movimentation] = Field(
        nullable=True,
        title='Process movimentations',
        example=[
            {
                'date': '22/02/2021',
                'description': 'Remetido recurso eletrônico ao Tribunal de Justiça/Turma de recurso',
            }
        ],
    )


class ProcessOut(Process):
    created_at: datetime = Field(
        default_factory=datetime.now, title='Creation date'
    )

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class ProcessIn(BaseSchemaMixin):
    process_number: str = Field(
        ..., title='Process number', example='07108025520188020001'
    )
