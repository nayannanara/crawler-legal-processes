from unittest import mock

import pytest
import sqlalchemy

from core.contrib.exceptions import DatabaseException, ObjectNotFound
from core.processes.schemas import Movimentation, ProcessOut


async def test_usecases_post_processes_should_return_success(
    process_usecase, process_in, db_session, mock_scraping_run
):
    result = await process_usecase.create(process_in, db_session)

    assert isinstance(result[0], ProcessOut)
    assert isinstance(result[0].movimentations[0], Movimentation)
    assert ('1º Grau' or '2º Grau') in [i.degree for i in result]


@mock.patch('sqlalchemy.ext.asyncio.AsyncSession.commit')
async def test_usecases_post_processes_should_return_raise(
    mock_commit, process_usecase, process_in, db_session, mock_scraping_run
):
    mock_commit.side_effect = sqlalchemy.exc.IntegrityError(
        mock.MagicMock(), mock.MagicMock(), mock.MagicMock()
    )

    with pytest.raises(DatabaseException) as exc:
        await process_usecase.create(process_in, db_session)

    assert isinstance(exc.value, DatabaseException)
    assert (
        'Ocorreu um erro ao inserir o dado no banco de dados.'
        in exc.value.message
    )


@pytest.mark.usefixtures('create_processes')
async def test_usecases_get_processes_should_return_success(
    process_usecase, process_number_tjal, db_session
):
    result = await process_usecase.get(process_number_tjal, db_session)

    assert isinstance(result, ProcessOut)
    assert result.process_number == '07108025520188020001'
    assert isinstance(result.movimentations[0], Movimentation)


async def test_usecases_get_processes_should_not_found(
    process_usecase, process_number_tjal, db_session
):

    with pytest.raises(ObjectNotFound) as exc:
        await process_usecase.get(process_number_tjal, db_session)

    assert isinstance(exc.value, ObjectNotFound)
    assert (
        exc.value.message
        == 'Process not found for number: 07108025520188020001'
    )


@pytest.mark.usefixtures('create_processes')
async def test_usecases_query_processes_should_return_success(
    process_usecase, db_session
):
    result = await process_usecase.query(db_session)

    assert isinstance(result[0], ProcessOut)
    assert len(result) > 1


async def test_usecases_query_processes_should_return_empty_list(
    process_usecase, db_session
):
    result = await process_usecase.query(db_session)

    assert result == []
