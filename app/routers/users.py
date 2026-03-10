from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import select

router = APIRouter()


@router.post("/login", response_model=UserReadSchema)
async def login(data: UserCreateSchema, db: Session = Depends(get_db)):

    get_user = select(UserModel).where(UserModel.email == data.email)
    user = db.scalars(get_user).one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    return user


@router.post("/register", response_model=UserReadSchema)
async def register(data: UserCreateSchema, db: Session = Depends(get_db)):

    query = select(UserModel).where(UserModel.email == data.email)
    existing_user = db.scalars(query).one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST ,
            detail="User already exists"
        )

    new_user = UserModel(
        username=data.username,
        email=data.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
