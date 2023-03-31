from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from core.configs.deps import get_session
from core.contrib.exceptions import DatabaseException, ObjectNotFound
from core.processes.schemas import ProcessIn, ProcessOut
from core.processes.usecases import ProcessUseCase

router = APIRouter()


@router.post(
    path='',
    summary='Create a new Process',
    status_code=status.HTTP_201_CREATED,
)
async def post(
    process_in: ProcessIn = Body(...),
    use_case: ProcessUseCase = Depends(),
    db_session: AsyncSession = Depends(get_session),
    response_model=list[ProcessOut]
) -> list[ProcessOut]:
    try:
        processes = await use_case.create(
            process_in=process_in, db_session=db_session
        )
    except DatabaseException:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER)

    return processes


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ProcessOut]
)
async def query(
    use_case: ProcessUseCase = Depends(),
    db_session: AsyncSession = Depends(get_session),
) -> list[ProcessOut]:
    processes = await use_case.query(db_session=db_session)

    return processes


@router.get(
    '/{process_number}',
    status_code=status.HTTP_200_OK,
    response_model=ProcessOut,
)
async def get(
    process_number: str,
    use_case: ProcessUseCase = Depends(),
    db_session: AsyncSession = Depends(get_session),
) -> ProcessOut:
    try:
        process: ProcessOut = await use_case.get(
            process_number=process_number, db_session=db_session
        )
    except ObjectNotFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f'Process not found for number: {process_number}',
        )

    return process
