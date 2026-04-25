from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.middlewares import RequestCounterMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Все нужные модели должны быть импортированы перед запуском

    # Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(RequestCounterMiddleware)

app.include_router(api_router)

# import uvicorn
# uvicorn.run(app, port=8080, reload=True)
