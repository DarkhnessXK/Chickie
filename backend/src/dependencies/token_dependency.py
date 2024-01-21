from fastapi import Depends

from typing import Annotated
from src.api.security import oauth2_scheme
TokenDependency = Annotated[str, Depends(oauth2_scheme)]