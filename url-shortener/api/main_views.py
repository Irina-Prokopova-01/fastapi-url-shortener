from datetime import date

from fastapi import (
    APIRouter,
    Request,
)
from starlette.responses import HTMLResponse

from core.config import BASE_DIR
from templating import templates

router = APIRouter(
    tags=["Read Root"],
)


@router.get(
    "/",
    response_class=HTMLResponse,
    name="home",
    include_in_schema=False,
)
def home_page(
    request: Request,
) -> HTMLResponse:
    context = {}
    features = [
        "Create short URLs",
        "Track all redirects",
        "Real-time statistics",
        "Shared management",
    ]
    context.update(
        features=features,
    )
    # print(f'"Контекст":{context}')
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context=context,
    )

@router.get(
    "/about",
    name="about",
    include_in_schema=False,
)
def about_page(
    request: Request
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="about.html",
    )