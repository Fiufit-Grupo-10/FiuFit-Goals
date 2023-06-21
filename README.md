![ci](https://github.com/Fiufit-Grupo-10/FiuFit-Goals/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/Fiufit-Grupo-10/FiuFit-Goals/branch/main/graph/badge.svg?token=OINqsRu8Fg)](https://codecov.io/gh/Fiufit-Grupo-10/FiuFit-Goals)
# FiuFit-Goals

Microservice goals implementation for Fiufit application

## Running dev enviroment:

To set up the development environment for this microservice, you need to have Docker and Docker Compose installed on your machine.
### 1. Clone this repository

```bash
git clone git@github.com:Fiufit-Grupo-10/FiuFit-Goals.git
```
### 2. Navigate to the cloned repository and execute

```bash
sudo docker-compose -f docker-compose-testing.yml up --build
```

## To run tests or other commands on the container:

```bash
sudo docker-compose -f docker-compose-testing.yml exec <command>
```
### Examples

To run tests

```bash
docker-compose -f docker-compose-testing.yml exec web pytest -vv
```
or
```bash
docker-compose -f docker-compose-testing.yml run --rm tests
```
