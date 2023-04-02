from fastapi import APIRouter

router = APIRouter(prefix='/test')


@router.get('/')
def index():
    return {}
