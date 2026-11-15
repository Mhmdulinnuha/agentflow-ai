from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    @staticmethod
    def get_all(db: Session):
        statement = select(User)
        
        return db.scalars(statement).all()
    @staticmethod 
    def get_by_id(db: Session, user_id: int):
        statement = select(User).where(User.id == user_id)
        return db.scalar(statement)