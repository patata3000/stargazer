# Stargazer

## Description


## Content

Misc:

- `Dockerfile`: Define simple docker image.
- `pyproject.toml`: Project technical description/dependencies.
- `flake.*`: Files used for Nixos (Not important).

## Start the project

You need to build the docker image then run the container with:

```bash
docker --debug build --no-cache -t interproccom .
docker run --name myupciti -t interproccom:latest
```
## Run the tests

Create a virtual environment with your prefered tool. Eg: `venv`

Install poetry in the virtual environment and install the project.

```bash
pip install poetry
poetry install
pytest
```
