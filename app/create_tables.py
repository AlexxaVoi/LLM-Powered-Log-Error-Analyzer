from .database import engine
from .models.base import BaseModel

BaseModel.metadata.create_all(bind=engine)
