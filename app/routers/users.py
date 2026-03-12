from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import select

router = APIRouter()


@router.post("/login", response_model=UserReadSchema)
async def login(data: UserCreateSchema, db: Session = Depends(get_db)):

    get_user = select(UserModel).where(
        UserModel.username == data.username and UserModel.password == data.password)
    user = db.scalars(get_user).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    return user


@router.post("/register", response_model=UserReadSchema)
async def register(data: UserCreateSchema, db: Session = Depends(get_db)):

    query = select(UserModel).where(UserModel.username == data.username)
    existing_user = db.scalars(query).one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="User already exists"
        )

    new_user = UserModel(
        username=data.username,
        password=data.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
