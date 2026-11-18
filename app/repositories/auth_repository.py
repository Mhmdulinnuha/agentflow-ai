
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.user import User


class AuthRepository:

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str,
    ):
        return db.scalar(
            select(User).where(
                User.email == email
            )
        )

    @staticmethod
    def get_user_by_id(
        db: Session,
        user_id: int,
    ):
        return db.get(User, user_id)

    @staticmethod
    def create_user(
        db: Session,
        user: User,
    ):
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def create_refresh_token(
        db: Session,
        refresh_token: RefreshToken,
    ):
        db.add(refresh_token)
        db.flush()
        return refresh_token

    @staticmethod
    def get_refresh_token_for_update(
        db: Session,
        token_hash: str,
    ):
        statement = (
            select(RefreshToken)
            .where(
                RefreshToken.token_hash == token_hash
            )
            .with_for_update()
        )

        return db.scalar(statement)
