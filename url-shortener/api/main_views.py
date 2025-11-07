from fastapi import (
    Request,
    APIRouter,
)

router = APIRouter(
    tags=["Read Root"],
)


@router.get("/")
def read_root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "massage": "Hello {name}",
        "docs": str(docs_url),
    }
