from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import settings
from storage.short_urls import ShortUrlsStorage


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncIterator[None]:
    # действия до запуска приложения
    # ставим эту функцию на паузу на время работы приложения
    app.state.short_urls_storage = ShortUrlsStorage(
        hash_name=settings.redis.collections_name.short_urls_hash)
    yield
    # выполняем завершение работы
    # закрываем соединения, финально сохраняем файлы
