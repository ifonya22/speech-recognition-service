from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api.v1.html import content

router = APIRouter()


@router.get("/")
async def main():
    return HTMLResponse(content=content)
