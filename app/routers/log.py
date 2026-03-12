from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.schemas.log import LogCreateSchema, LogReadSchema
from app.schemas.log_analysis import AnalysisReadSchema
from app.models.log import LogModel
from app.models.log_analysis import LogAnalysisModel
from app.database import get_db
from app.services.log_parser import clean_log, file_transformation
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.constants import ALLOWED_EXTENSIONS


router = APIRouter()


@router.get("", response_model=List[LogReadSchema])
async def log_history(user_id: int, db: Session = Depends(get_db)):
    query = select(LogModel).where(LogModel.user_id == user_id)
    all_logs = db.scalars(query).all()

    return all_logs


@router.post("/upload", response_model=LogReadSchema)
async def upload_log(
        user_id: int,
        file: UploadFile = File(...),
        db: Session = Depends(get_db)):
    if not file.filename.endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt, .log and .csv files are allowed"
        )

    content = await file.read()
    clean_log_text = file_transformation(content)
    if not clean_log_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No errors found in the provided log text"
        )

    log_data = LogModel(
        user_id=user_id,
        log_text=clean_log_text
    )
    db.add(log_data)
    db.commit()
    db.refresh(log_data)
    return log_data


@router.post("/raw", response_model=LogReadSchema)
async def upload_raw(data: LogCreateSchema, db: Session = Depends(get_db)):
    clean_log_text = clean_log(data.log_text)
    if not clean_log_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No errors found in the provided log text"
        )

    log_data = LogModel(
        user_id=data.user_id,
        log_text=clean_log_text
    )
    db.add(log_data)
    db.commit()
    db.refresh(log_data)
    return log_data


@router.post("/{log_id}/analysis", response_model=AnalysisReadSchema)
async def run_ai_analysis(log_id: int, user_id: int, db: Session = Depends(get_db)):
    query = select(LogModel).where(LogModel.id == log_id, LogModel.user_id == user_id)
    log_to_analyze = db.scalars(query).one_or_none()

    if not log_to_analyze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found or access denied")

    # ...write LLM logic
    new_analysis = LogAnalysisModel(
        log_id=log_id,
        issue="Error in Database",
        root_cause="Перевищено ліміт підключень",
        solution="Перевірте налаштування pool_size у вашому engine"
    )

    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    return new_analysis
