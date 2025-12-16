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
)
def read_root(
) -> str:
    return (BASE_DIR / "pages" / "home.html").read_text()
