from fastapi import FastAPI

from core.configs.settings import settings
from core.routers import api_router

app = FastAPI(title='Processes API')
app.include_router(api_router, prefix=settings.API_VERSION)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app', host='0.0.0.0', port=8000, log_level='info', reload=True
    )
