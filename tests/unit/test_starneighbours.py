"""Integration testing for PubSub messaging."""

from multiprocessing.pool import ThreadPool
from unittest.mock import MagicMock, Mock, patch

from github import Github
from github.GithubObject import GithubObject
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from pytest import fixture, MonkeyPatch

from app.crud.github_client import make_github_app_client
from app.crud.starneighbours import (
    build_repo_username_mapping,
    build_result,
    fetch_stargazers,
    fetch_user_starred_repos,
    get_page_iterator,
    get_starneighbours,
)
from app.schemas.stargazer import Starneighbour


@fixture
def mapping():
    return {
        "repo_1": ["carrot", "raspberry", "pie"],
        "repo_2": ["apricot", "pie"],
    }


def test_build_result(mapping: dict[str, list[str]]):
    result = build_result(mapping)
    assert result == [
        Starneighbour(repo="repo_1", stargazers=["carrot", "raspberry", "pie"]),
        Starneighbour(repo="repo_2", stargazers=["apricot", "pie"]),
    ]


@fixture
def stargazer_repos():
    return [
        (
            MagicMock(login="jean-pierre"),
            [
                MagicMock(full_name="ouistiti"),
                MagicMock(full_name="avion"),
            ],
        ),
        (
            MagicMock(login="jean-marc"),
            [
                MagicMock(full_name="ouistiti"),
                MagicMock(full_name="citrus"),
            ],
        ),
        (
            MagicMock(login="jean-chaine"),
            [
                MagicMock(full_name="avion"),
            ],
        ),
    ]


def test_build_repo_username_mapping(
    stargazer_repos: list[tuple[NamedUser, list[Repository]]]
):
    result = build_repo_username_mapping(stargazer_repos)
    assert result == {
        "avion": ["jean-pierre", "jean-chaine"],
        "citrus": ["jean-marc"],
        "ouistiti": ["jean-pierre", "jean-marc"],
    }


@fixture
def paginated_objects():
    return MagicMock(total_count=303)


def test_get_page_iterator[T: GithubObject](paginated_objects: PaginatedList[T]):
    result = get_page_iterator(paginated_objects)
    for i, iterator_i in enumerate(result):
        assert i == iterator_i


@fixture
def stargazer():
    mock = Mock(get_starred=lambda: ["malabar", "carambar", "schtroumpf"])
    mock.name = "userify"
    return mock


def test_fetch_user_starred_repos(stargazer: NamedUser):
    result = fetch_user_starred_repos(stargazer)
    assert result[0].name == "userify"
    assert result[1] == ["malabar", "carambar", "schtroumpf"]


@fixture
def github_client():
    return Mock()


@fixture
def pool():
    return MagicMock(map=lambda _a, _b: [["mandarine"], ["pamplemousse", "citouille"]])


@fixture
def user():
    return "Jacques"


@fixture
def repo():
    return "Chirac"


def test_fetch_stargazers(
    github_client: MagicMock, pool: MagicMock, user: str, repo: str
):
    result = fetch_stargazers(github_client, pool, user, repo)
    assert github_client.get_repo.called
    assert result == ["mandarine", "pamplemousse", "citouille"]


@patch("app.crud.starneighbours.make_github_app_client")
@patch("app.crud.starneighbours.fetch_stargazers")
@patch("app.crud.starneighbours.build_result", return_value=["moby", "gaby"])
def test_get_starneighbours(
    client_mock: MagicMock,
    fetch_stargazers_mock: MagicMock,
    build_result_mock: MagicMock,
    user: str,
    repo: str,
):
    result = get_starneighbours(user, repo)
    assert client_mock.called
    assert fetch_stargazers_mock.called
    assert build_result_mock.called
    assert result == ["moby", "gaby"]
