from fastapi import APIRouter

from app.crud.starneighbours import get_starneighbours
from app.schemas.stargazer import Starneighbour

router = APIRouter()


@router.get("/{user}/{repo}/starneighbours")
async def read_starneighbours(user: str, repo: str) -> list[Starneighbour]:
    """
    Retrieve all the starneighbours of a repo.

        Args:
            user: The name of the owner of the stargazed repository.
            repo: The name of the stargazed repository.

        Return:
            List of all the Starneighbours.
    """
    return get_starneighbours(user, repo)
