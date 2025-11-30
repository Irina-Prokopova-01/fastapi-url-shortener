#FastAPI URL Shortener
[![Hello World](https://github.com/Irina-Prokopova-01/fastapi-url-shortener/actions/workflows/hello-actions.yaml/badge.svg)](https://github.com/Irina-Prokopova-01/fastapi-url-shortener/actions/workflows/hello-actions.yaml)
## Develop

Check Github Actions after any push.

Steps:

Right click "url-shortener"-> Mark Directory as -> Sources Root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```


### Install

Install packages:
```shell
uv install
```

## Run

Go to workdir:
```shell
cd url-shortener
```
Run dev server:
```shell
fastapi dev
```

## Snippets

```shell
 python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
