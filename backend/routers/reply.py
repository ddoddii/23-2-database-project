from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from database import create_server_connection, execute_query, execute_read_query
import re
from datetime import datetime

router = APIRouter(prefix="/api/post", tags=["posts"])


class AnswerCreate(BaseModel):
    content: str
