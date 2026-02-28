from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.db.models import User
from app.services.search.web_search import search_web

router = APIRouter(prefix="/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


@router.post("")
async def web_search(
    request: SearchRequest,
    current_user: User = Depends(get_current_user),
):
    results = await search_web(request.query, request.max_results)
    return {"results": results}
