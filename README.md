# Stargazer

## Description

Implementation of a API route that retrieves the "starneighbours" of a repo.
A starneighbour of a repo has at least one user that starred both repo.

You can find the description of the problem here:
https://mergify.notion.site/Stargazer-4cf5427e34a542f0aee4e829bb6d9035

## Content

- `src`: All the source code of the `fastapi` app.
- `tests`: Unit tests for the project.
- `pyproject.toml`: Project technical description/dependencies.
- `private_key.pem`: Used to connect to github API as a Github App. This
should not be in the repo but be set at deployment by another mean.
- `flake.*`: Files used for Nixos (Not important).

## Start the project

You can run the project by installing `uv` and by running:

```bash
uv run fastapi run src/app/app.py
```

## Run the tests

You can create a virtual env with `uv` then run:

```bash
pytest
```

## Limit of the project

### Missing exercise

First and foremost, I've not implemented the second part about
authentication. I was planning to use `authlib` and was not sure
yet if I'd need a database or if a stateful server would be enough.

I spent quite a while on the first part and I'm over the time limit.

### Status of the Starneighbour part

This project uses `pygithub` which permits to create a client to Github
API.

It uses a `ThreadPool` to run requests in parallel.

It doesn't use any DB.

One request can be very long as all stargazers must be fetched, then all
the starred repos of each stargazers before issuing a response. So an
~(S x M / 100) requests are necessary to fetch all data. With:

- S: Number of stargazers of the main repo,
- M: Mean number of starred repo by each stargazer,
- 100: Max number of elements in a request.

This is rapidly unusable as is. One request could take days to complete for
big repos. With Github rate limits, we need to look for other solutions than
simply crank up the number of parallel threads.

### Possible improvements

- Biggest improvements could come from saving locally all the already seen
users and repos. For already fetched users, requests would not need to be sent
again.
- Github gives webhooks which could be useful if we'd like to stay updated
with already saved repos or users.
- Do we need to be exhaustive with the results. If not, we could make some
compromises with what we send back. We can probably find some algorithms
that are more efficient with relaxed constraints. For example, by limiting
stargazers to 100 starred repos.
- We can probably gain an order of magnitude by tweaking the number of parallel
processes before being kicked by rate limits.
- We can also try create multiple Github Apps behind proxies to be able to go
around the rate limits if it's a necessity.
- Parallelisation could be done on all tasks by starting fetching for repos
before retrieving every stargazers. It would not be a big win by itself but
coupled with, for example, the 3rd point, it could give incomplete responses
much faster.
- ...
