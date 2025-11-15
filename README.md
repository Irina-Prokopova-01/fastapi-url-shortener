#FastAPI URL Shortener
## Develop

Step:

Right click "url-shortener"-> Mark Directory as -> Sources Root

### Install dependencies

Install all packages:
```shell
uv install
```

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
