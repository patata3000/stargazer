from github import Github, GithubIntegration
from github.Auth import AppAuth

from app.config import settings


def make_github_api() -> Github:
    """Build Github API client by authenticating as an Github App.

    Return:
        An authenticated `Github` client.
    """
    app_token = AppAuth(settings.CLIENT_ID, settings.PRIVATE_KEY)
    gi = GithubIntegration(
        auth=app_token,
        per_page=settings.PER_PAGE,
    )
    return gi.get_installations()[0].get_github_for_installation()
