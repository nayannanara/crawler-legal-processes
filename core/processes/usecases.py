import sqlalchemy
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.configs.deps import get_session
from core.contrib.exceptions import DatabaseException, ObjectNotFound
from core.processes.models import Movimentation, Process
from core.processes.schemas import ProcessIn, ProcessOut
from core.scrapper.selenium.app import ProcessesScraping


class ProcessUseCase:
    async def create(
        self: 'ProcessUseCase',
        process_in: ProcessIn,
        db_session: AsyncSession = Depends(get_session),
    ) -> list[ProcessOut]:
        scraping = ProcessesScraping()

        try:
            payload = scraping.run(input=process_in.process_number)
            processes = [ProcessOut(**data) for data in payload]

            for process in processes:
                process_model = Process(
                    **process.dict(exclude={'movimentations', 'class_'}),
                    class_=process.class_,
                    movimentations=[
                        Movimentation(**movimentation.dict())
                        for movimentation in process.movimentations
                    ],
                )
                db_session.add(process_model)
                await db_session.commit()

                logger.info(f'Processo criado: {process}')
        except sqlalchemy.exc.IntegrityError as exc:
            raise DatabaseException(
                message=f'An unexpected error occurred with the database with error: {exc}'
            )

        return [ProcessOut.from_orm(process) for process in processes]

    async def query(
        self: 'ProcessUseCase', db_session: AsyncSession = Depends(get_session)
    ) -> list[ProcessOut]:
        processes: list[ProcessOut] = (
            (await db_session.execute(select(Process))).scalars().all()
        )
        processes = [ProcessOut.from_orm(process) for process in processes]

        return processes

    async def get(
        self: 'ProcessUseCase',
        process_number: str,
        db_session: AsyncSession = Depends(get_session),
    ) -> ProcessOut:

        process = (
            (
                await db_session.execute(
                    select(Process)
                    .filter_by(process_number=process_number)
                    .order_by(Process.created_at.desc())
                )
            )
            .scalars()
            .first()
        )

        if not process:
            raise ObjectNotFound(
                message=f'Process not found for number: {process_number}'
            )

        return ProcessOut.from_orm(process)
