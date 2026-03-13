from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from app.schemas.log import LogCreateSchema, LogReadSchema
from app.schemas.log_analysis import AnalysisReadSchema
from app.models.user import UserModel
from app.models.log import LogModel
from app.models.log_analysis import LogAnalysisModel
from app.database import get_db
from app.services.log_parser import clean_log, file_transformation
from app.services.ai_processes import get_ai_analysis
from app.services.auth import get_current_user
from app.constants import ALLOWED_EXTENSIONS
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select


router = APIRouter()


@router.get("",
            summary="Get history of query",
            description="This method allows you to view the"
            " current user's query history with the LLM",
            response_model=List[LogReadSchema])
async def log_history(
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)):

    query = select(LogModel).where(LogModel.user_id == current_user.id)
    all_logs = db.scalars(query).all()
    return all_logs


@router.post("/upload",
             summary="Upload file with a log",
             description="Accepts .txt/.log/.csv "
             "files and saves them to the database",
             response_model=LogReadSchema)
async def upload_log(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)):
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
        user_id=current_user.id,
        log_text=clean_log_text
    )
    db.add(log_data)
    db.commit()
    db.refresh(log_data)
    return log_data


@router.post("/raw",
             summary="Entering text with a log",
             description="Accepts enter text with "
             "log and saves them to the database",
             response_model=LogReadSchema)
async def upload_raw(
        data: LogCreateSchema,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)):

    clean_log_text = clean_log(data.log_text)
    if not clean_log_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No errors found in the provided log text"
        )

    log_data = LogModel(
        user_id=current_user.id,
        log_text=clean_log_text
    )
    db.add(log_data)
    db.commit()
    db.refresh(log_data)
    return log_data


@router.post("/{log_id}/analysis",
             summary="Analysis of the query",
             description="Analyzes the query and returns a response "
             "(issue, root_cause, solution) from the LLM model",
             response_model=AnalysisReadSchema)
async def run_ai_analysis(
        log_id: int,
        сurrent_user: UserModel = Depends(get_current_user),
        db: Session = Depends(get_db)):

    query = select(LogModel).where(
        LogModel.id == log_id,
        LogModel.user_id == сurrent_user.id)
    log_to_analyze = db.scalars(query).one_or_none()

    if not log_to_analyze:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Log not found or access denied"
        )

    ai_result = await get_ai_analysis(log_to_analyze.log_text)

    if not ai_result or ai_result.get("issue") == "AI Analysis Failed":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is currently unavailable or "
            "failed to process the log:( Please try again later.")

    new_analysis = LogAnalysisModel(
        log_id=log_id,
        issue=ai_result.get("issue"),
        root_cause=ai_result.get("root_cause"),
        solution=ai_result.get("solution")
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis
