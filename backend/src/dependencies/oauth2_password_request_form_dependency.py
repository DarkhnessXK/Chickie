from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated


Oauth2PasswordRequestFormDependency = Annotated[
    OAuth2PasswordRequestForm, Depends()
]
