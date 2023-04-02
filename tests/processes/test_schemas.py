import pytest

from core.processes.schemas import Movimentation, ProcessIn, ProcessOut


@pytest.mark.parametrize(
    'payload',
    [
        {'process_number': '00703379120088060001'},
        {'process_number': '07108025520188020001'},
    ],
)
async def test_schemas_process_in(payload):
    process_in = ProcessIn.parse_obj(payload)

    assert process_in.process_number == payload['process_number']


async def test_schemas_process_out(payload):

    processes = [ProcessOut.parse_obj(data) for data in payload]

    assert processes[0].process_number == '07108025520188020001'
    assert isinstance(processes[0].movimentations[0], Movimentation)
