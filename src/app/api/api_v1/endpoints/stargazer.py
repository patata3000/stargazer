from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.starneighbours import get_starneighbours
from app.schemas.stargazer import Starneighbour

router = APIRouter()


@router.get("/{user}/{repo}/starneighbours")
async def read_starneighbours(user: str, repo: str) -> list[Starneighbour]:
    """Retrieve all the starneighbours of a repo.

    Args:
        user: The name of the owner of the stargazed repository.
        repo: The name of the stargazed repository.

    Return:
        List of all the Starneighbours.
    """
    return get_starneighbours(user, repo)


# @router.get("/", response_model_exclude_none=True)
# async def read_contacts_endpoint(
#     skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)
# ) -> list[Starneighbours]:
#     return await get_contacts(db=db, skip=skip, limit=limit)
