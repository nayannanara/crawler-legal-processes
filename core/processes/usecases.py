import sqlalchemy
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.configs.deps import get_session
from core.contrib.exceptions import DatabaseException, ObjectNotFound
from core.processes.models import Process
from core.processes.schemas import ProcessIn, ProcessOut
from scrapper.selenium.app import scraping


class ProcessUseCase:
    async def create(
        self: 'ProcessUseCase',
        process_in: ProcessIn,
        db_session: AsyncSession = Depends(get_session),
    ) -> ProcessOut:

        try:
            process = scraping.run(process_in.process_number)
            breakpoint()
            db_session.add(ProcessOut(**process))
            await db_session.commit()
        except sqlalchemy.exc.IntegrityError as exc:
            raise DatabaseException(
                message=f'An unexpected error occurred with the database with error: {exc}'
            )

        return ProcessOut.from_orm(process)

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
                    select(Process).filter_by(process_number=process_number)
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
