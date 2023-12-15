from http import HTTPStatus
from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    email: str
    username: str
    password: str


class OTPUserDTO(UserDTO):
    otp: int


class AuthServiceDTO(BaseModel):
    status: HTTPStatus
    message: Optional[str] = None
