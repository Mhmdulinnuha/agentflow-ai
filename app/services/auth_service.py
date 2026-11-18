
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_refresh_token,
    create_access_token,
    hash_refresh_token,
    get_refresh_token_expiry,
)

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.auth_repository import AuthRepository


class AuthService:

    @staticmethod
    def _create_token_pair(db: Session, user: User):
        raw_refresh_token = create_refresh_token()

        refresh_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(raw_refresh_token),
            expires_at=get_refresh_token_expiry(),
        )

        AuthRepository.create_refresh_token(
            db,
            refresh_record,
        )
        

        access_token = create_access_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": raw_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    @staticmethod
    def register(db: Session, data):
        existing_user = AuthRepository.get_user_by_email(
            db,
            data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=hash_password(data.password),
            is_active=True,
        )

        try:
            AuthRepository.create_user(db, user)
            
            db.flush()

            tokens = AuthService._create_token_pair(
                db,
                user,
            )

            db.commit()
            return tokens

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def login(db: Session, data):
        user = AuthRepository.get_user_by_email(
            db,
            data.email,
        )

        if not user or not verify_password(
            data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        try:
            tokens = AuthService._create_token_pair(
                db,
                user,
            )

            db.commit()
            return tokens

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def refresh(db: Session, raw_token: str):
        token_hash = hash_refresh_token(raw_token)

        try:
            stored_token = (
                AuthRepository.get_refresh_token_for_update(
                    db,
                    token_hash,
                )
            )

            now = datetime.now(timezone.utc).replace(
                tzinfo=None
            )

            if (
                not stored_token
                or stored_token.revoked_at is not None
                or stored_token.expires_at <= now
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired refresh token",
                )

            user = AuthRepository.get_user_by_id(
                db,
                stored_token.user_id,
            )

            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User account is unavailable",
                )

            # Cabut token lama sebelum membuat token baru.
            stored_token.revoked_at = now

            tokens = AuthService._create_token_pair(
                db,
                user,
            )

            db.commit()
            return tokens

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def logout(db: Session, raw_token: str):
        token_hash = hash_refresh_token(raw_token)

        try:
            stored_token = (
                AuthRepository.get_refresh_token_for_update(
                    db,
                    token_hash,
                )
            )

            if (
                stored_token
                and stored_token.revoked_at is None
            ):
                stored_token.revoked_at = (
                    datetime.now(timezone.utc).replace(
                        tzinfo=None
                    )
                )

            db.commit()

        except Exception:
            db.rollback()
            raise
