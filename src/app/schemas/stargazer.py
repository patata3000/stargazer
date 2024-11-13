from pydantic import BaseModel


class Starneighbour(BaseModel):
    repo: str
    stargazers: list[str]
