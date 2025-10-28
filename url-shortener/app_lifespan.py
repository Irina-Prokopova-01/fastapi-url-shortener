from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from api.api_v1.short_url.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # действия до запуска приложения
    # ставим эту функцию на паузу на время работы приложения
    yield
    # выполняем завершение работы
    # закрываем соединения, финально сохраняем файлы.
