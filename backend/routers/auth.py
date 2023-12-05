from datetime import datetime, timedelta
from typing import Annotated, Optional

import starlette.status as status
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from database import *

router = APIRouter(prefix="", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "e67cb6e960b18ce8ec8f683d28997ff83bada88df9321e52079f712c4e4c850e"
ALGORITHM = "HS256"


class CreateUserRequest(BaseModel):
    username: str
    password: str
    name: str
    type: Optional[int] = 0
    birth: Optional[datetime] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginUserRequest(BaseModel):
    username: str
    password: str


@router.post("/api/user/create")
async def create_user(create_user_request: CreateUserRequest):
    check_duplicate_username(create_user_request.username)
    hashed_password = bcrypt_context.hash(create_user_request.password)
    connection = create_server_connection()
    query = f"""
    INSERT INTO users (username ,password, name, type, birth, sex, address, phone)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        create_user_request.username,
        hashed_password,
        create_user_request.name,
        create_user_request.type,
        create_user_request.birth,
        create_user_request.sex,
        create_user_request.address,
        create_user_request.phone,
    )

    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
    except mysql.connector.Error as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.post("/api/user/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    token = create_access_token(
        user["username"], user["user_id"], timedelta(minutes=60)
    )
    return {"access_token": token, "token_type": "bearer", "username": user["username"]}


@router.get("/users", status_code=status.HTTP_200_OK)
def get_all_users():
    connection = create_server_connection()
    query = """
    SELECT username FROM users;
    """
    user_names = execute_read_query(connection, query)
    connection.close()
    user_names_list = [name["username"] for name in user_names]
    return {"users": user_names_list}


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    token = create_access_token(
        user["username"], user["user_id"], timedelta(minutes=60)
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        return {
            "username": username,
            "id": user_id,
        }
    except JWTError:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )


def create_access_token(username: str, user_id: int, expires_data: timedelta):
    encode = {"sub": username, "id": user_id}
    expire = datetime.utcnow() + expires_data
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM Users WHERE username = %s;"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if not user:
        return False

    hashed_password = user["password"]
    if not bcrypt_context.verify(password, hashed_password):
        return False
    return user


def check_duplicate_username(request_username):
    connection = create_server_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT username FROM users WHERE username = %s;
    """
    cursor.execute(query, (request_username,))
    existing_user = cursor.fetchone()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
