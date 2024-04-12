# social-media-django

## Run using venv
Instructions on running the application

1. Pull the repository
2. Create a virtual env using

    `python -m venv /path/to/your/env`
3. Activate the env using

    `source /path/to/env/bin activate/`

4. Run application using

    `python manage.py runserver`

    the app will be availble on `127.0.0.1:8000`


## Run using docker

You can simply run

`docker compose up`

and the app will be available on `127.0.0.1:8000`

The built image of the application is pushed to my personal docker hub.

## Using the app

To create and register a user, use `POST users/register/` endpoint. Sample payload for it looks like
```
{
    "first_name":"abhijit1",
    "last_name":"ghate1",
    "email": "a1@abc.co",
    "username": "a1@abc.co",
    "password":"12345"
}
```

This will result in getting an access token and refresh token. Make sure to use access token as `Bearer` token in protected requests.

e.g.
```
{
    "response": "Account has been created",
    "username": "a1@abc.co",
    "email": "a1@abc.co",
    "token": {
        "refresh":"eyJhb9 ...",
        "access": "eyJhbGciOiJ ..."
    }
}
```

If the token expires you need to acquire a new one using `POST users/login/` endpoint. Sample payload for it looks like
```
{
    "username": "0xref.r2psgpegj@example.com",
    "password": "12345"
}
```
*NOTE* : We are using username and email as one and the same field.
