from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.contrib.models import BaseModel


class Process(BaseModel):
    __tablename__ = 'processes'

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True, index=True
    )
    process_number: Mapped[str] = mapped_column(String, nullable=False)
    class_: Mapped[str] = mapped_column(String, nullable=True)
    area: Mapped[str] = mapped_column(String, nullable=True)
    topic: Mapped[str] = mapped_column(String, nullable=True)
    distribution_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True
    )
    judge: Mapped[str] = mapped_column(String, nullable=True)
    stock_price: Mapped[str] = mapped_column(String(), nullable=True)
    process_parties: Mapped[dict[str, list[str]]] = mapped_column(
        JSONB(), nullable=True
    )
    degree: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    movimentations: Mapped[list['Movimentation']] = relationship(
        'Movimentation', lazy='selectin'
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Movimentation(BaseModel):
    __tablename__ = 'movimentations'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    date: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    process_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey('processes.id'), nullable=False, index=True
    )
