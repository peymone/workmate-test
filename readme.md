<h1 align="center">work-mate test task</h1>

<p align="center">
    <img src="https://img.shields.io/badge/%20Python-3.11.3-blue?style=for-the-badge&logo=Python" alt="Python">
    <img src="https://img.shields.io/badge/%20SQLAlchemy-2.0.35-brightgreen?style=for-the-badge" alt="SQLAlchemy">
    <img src="https://img.shields.io/badge/%20FastAPI-0.114.2-brightgreen?style=for-the-badge" alt="FastAPI">
    <img src="https://img.shields.io/badge/pytest-8.3.3-brightgreen?style=for-the-badge" alt="Pyetst">
    <img src="https://img.shields.io/badge/pytest_asyncio-0.24.0-brightgreen?style=for-the-badge" alt="pytest_asyncio">
</p>

<p align="center">
    <img src="https://img.shields.io/github/downloads/peymone/workmate-test/total?style=social&logo=github" alt="downloads">
    <img src="https://img.shields.io/github/watchers/peymone/workmate-test" alt="watchers">
    <img src="https://img.shields.io/github/stars/peymone/workmate-test" alt="stars">
</p>


<h2>About</h2>

**_Test task from work-mate company:_** <a href="https://work-mate.ru/">**_work-mate_**</a> _Hi, HR_


**_Design a REST API for the administrator of an online kitten show. The API should have the following methods:_**

- _Getting a list of breeds_
- _Getting a list of all kittens_
- _Getting a list of kittens of a certain breed by filter._
- _Getting detailed information about a kitten._
- _Adding information about a kitten_
- _Changing information about a kitten_
- _Deleting information about a kitten_

_**Business logic:**_

_Each kitten should have – color, age (full months) and description.
If there is ambiguity in the task – the final decision remains with the candidate._

<h2>Deploy</h2>

> _**Don't look, just hire me**_

<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWdjYzE4aDc5a2RjcWJ6eXV5ZHo1dXJoY2ZnOWN2OGFsaG45OWNmNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L08EPJaIZuxlPUYy4N/giphy.gif" width="250px" height="150px"><br/><br/>

- _Downlocad latest release of application and unpack_
- _Open terminal in same directory with docker-compose.yml_
    - _Run following command to build and run container in detached mode:_ **_```docker-compose up -d```_**
- _Follow link to get swagger api:_ <a href="http://localhost:8000/docs">**_application link_**</a>
- _To stop container, run command (this will stops and delete container): **```docker-compose down -v```**_


<h2>Additional settings</h2>

_You can setup this application by change docker-compose file:_

- _environment_
    - _DATABASE_URL - url to cats database (db/cats.db by default)_
- _command - command for run application (here you can change host and port for server)_
- _ports - application mapping_

<br>

> **_P.S. Oh yeah, you haven't seen the tests because there aren't any._**
>> **_just a joke, they are launched at the container build stage_**

>> _**Of course you can use this: <a href=https://github.com/pytest-docker-compose/pytest-docker-compose>pytest-docker-compose</a>**_
>>> _**But for some reason it doesn't install. And I'm generally too lazy, bye!**_
