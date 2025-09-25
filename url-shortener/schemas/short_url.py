from typing import Annotated

from annotated_types import Len, MaxLen, MinLen
from pydantic import BaseModel, AnyHttpUrl


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str
    description: Annotated[
        str,
        MinLen(0),
        MaxLen(200),
    ] = ""


class ShortUrlCreate(ShortUrlBase):
    """Модель для создания сокращенной ссылки"""

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления информации
    о сокращенной ссылки
    """


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
