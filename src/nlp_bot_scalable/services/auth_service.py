from sqlalchemy.orm import Session

from nlp_bot_scalable.auth.jwt import create_access_token
from nlp_bot_scalable.auth.password import hash_password, verify_password
from nlp_bot_scalable.database.models import User


class AuthService:

    def register(
        self,
        db: Session,
        username: str,
        email: str,
        password: str,
    ):
        existing_user = (
            db.query(User)
            .filter(
                (User.username == username) |
                (User.email == email)
            )
            .first()
        )

        if existing_user:
            return {
                "success": False,
                "message": "Username or email already exists.",
            }

        user = User(
            username=username,
            email=email,
            password=hash_password(password),
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "success": True,
            "message": "Registration successful.",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
        }

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ):
        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None or not verify_password(password, user.password):
            return {
                "success": False,
                "message": "Invalid email or password.",
            }

        access_token = create_access_token(user.id, user.email)

        return {
            "success": True,
            "message": "Login successful.",
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "access_token": access_token,
            "token_type": "bearer",
        }
