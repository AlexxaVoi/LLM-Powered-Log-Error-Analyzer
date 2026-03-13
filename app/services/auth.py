from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.user import UserModel

security = HTTPBasic()


async def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)):

    query = select(UserModel).where(
        UserModel.username == credentials.username,
        UserModel.password == credentials.password
    )
    user = db.scalars(query).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
