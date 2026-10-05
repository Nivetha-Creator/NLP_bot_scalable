from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from nlp_bot_scalable.api.dependencies import get_db
from nlp_bot_scalable.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: int | None = None
    username: str | None = None
    email: str | None = None
    access_token: str | None = None
    token_type: str | None = None


@router.post("/register", response_model=AuthResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return auth_service.register(
        db,
        request.username,
        request.email,
        request.password,
    )


@router.post("/login", response_model=AuthResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return auth_service.login(
        db,
        request.email,
        request.password,
    )
