from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_users(db: Session):
        return UserRepository.get_all(db)
    @staticmethod
    def get_user(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id) 