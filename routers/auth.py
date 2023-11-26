from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from database import *
from pydantic import BaseModel, EmailStr, constr
from typing import Literal, Annotated, Optional
from datetime import datetime

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

bcrypt_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl= 'auth/token')

class CreateUserRequest(BaseModel):
    email_id: str
    password: str
    name: str
    type: Optional[int] = 0
    birth: Optional[datetime] = None
    sex: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    
class Token(BaseModel):
    access_token : str
    token_type : str
    
@router.post("/")
async def create_user(create_user_request : CreateUserRequest):
    hashed_password =  bcrypt_context.hash(create_user_request.password)
    connection = create_server_connection()
    query = f"""
    INSERT INTO user (email_id password, name, type, birth, sex, address, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        create_user_request.email_id,
        hashed_password,
        create_user_request.name,
        create_user_request.type,
        create_user_request.birth,
        create_user_request.sex,
        create_user_request.address,
        create_user_request.phone
    )
    
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
    except mysql.connector.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {e}")


