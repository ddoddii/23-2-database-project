from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, Field


router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

