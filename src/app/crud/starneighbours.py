import logging
from collections.abc import Iterator
from multiprocessing.pool import ThreadPool

from github import Github
from github.GithubObject import GithubObject
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList
from github.Repository import Repository

from app.config import settings
from app.schemas.stargazer import Starneighbour

from .github_client import make_github_api

logger = logging.getLogger(__name__)


def get_starneighbours(user: str, repo: str) -> list[Starneighbour]:
    """Retrieve all Starneighbours of a Github repository.

    A Starneighbour is another repository that has been starred by a user
    that starred the current repository.

    Args:
        user: The name of the owner of the stargazed repository.
        repo: The name of the stargazed repository.

    Return:
        List of all the Starneighbours.
    """
    pool = ThreadPool(processes=4)
    main_repo_stargazers: list[NamedUser] = fetch_stargazers(pool, user, repo)
    stargazed_repos = pool.map(fetch_user_starred_repos, main_repo_stargazers)
    mapping_repos_stargazers = build_repo_username_mapping(stargazed_repos)
    result = build_result(mapping_repos_stargazers)
    logger.debug(
        "Results -> nb users: %d ; nb repos: %d", len(main_repo_stargazers), len(result)
    )
    return result


def fetch_stargazers(pool: ThreadPool, user: str, repo: str) -> list[NamedUser]:
    """Retrieve the stargazers of the current repo.

    Args:
        pool: Use an already initialized threadpool to make parallel fetching.
        user: The name of the owner of the stargazed repository.
        repo: The name of the stargazed repository.

    Return:
        List of all stargazers of the `repo`.
    """
    api: Github = make_github_api()
    main_repo = api.get_repo(f"{user}/{repo}")
    stargazer_result = []
    logger.debug("Fetching stargazer")
    stargazers: PaginatedList[NamedUser] = main_repo.get_stargazers()
    page_iterator = get_page_iterator(stargazers)
    for stargazer_list in pool.map(stargazers.get_page, page_iterator):
        logger.debug("Fetched %s stargazers", len(stargazer_list))
        stargazer_result.extend(stargazer_list)
    return stargazer_result


def fetch_user_starred_repos(
    stargazer: NamedUser,
) -> tuple[NamedUser, list[Repository]]:
    """Fetch all repositories starred by a user.

    Args:
        stargazer: Said user.

    Return:
        A tuple of a user and all its starred repos.
    """
    repos = []
    for starred_repo in stargazer.get_starred():
        repos.append(starred_repo)
    return (stargazer, repos)


def get_page_iterator[
    T: GithubObject
](paginated_objects: PaginatedList[T]) -> Iterator[int]:
    """A small generator to iterate over paginated objects.

    Args:
        paginated_objects: Paginated objects coming from Github API.
    Return:
        Iterator over page numbers.
    """
    total_count = paginated_objects.totalCount
    for page_nb in range((total_count // settings.PER_PAGE) + 1):
        yield page_nb


def build_repo_username_mapping(
    stargazer_repos: list[tuple[NamedUser, list[Repository]]]
) -> dict[str, list[str]]:
    """Create a mapping between a repo and its stargazers.

    Args:
        stargazer_repos: List of all the stargazers and their stargazed repos.
    Return:
        A mapping between a repo full name and its stargazers.
    """
    mapping = {}
    for named_user, repo_list in stargazer_repos:
        username = named_user.login
        logger.debug("Fetched %d repository for user '%s'", len(repo_list), username)
        for repository in repo_list:
            if username is None:
                logger.debug("Skipping %s, invalid username", named_user)
                continue
            mapping.setdefault(repository.full_name, list()).append(username)
    return mapping


def build_result(mapping: dict[str, list[str]]) -> list[Starneighbour]:
    """Build the final list of all the stargazed repos and their stargazers.

    Args:
        mapping: A mapping between a repo full name and its stargazers.

    Return:
        List of all the Starneighbours.
    """
    result = []
    for repo_name, users in mapping.items():
        result.append(Starneighbour(repo=repo_name, stargazers=users))
    return result
