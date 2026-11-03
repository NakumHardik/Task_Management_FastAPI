from fastapi import HTTPException, status, Request, BackgroundTasks
from src.user.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta, timezone
from src.utils.mail import send_emails
from src.utils.helper import is_authenticated as helper_is_authenticated


password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return password_hash.verify(plain_password, hash_password)


def register(body: UserSchema, db: Session, bg_task: BackgroundTasks):
    # Check whether username already exists
    is_user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()

    if is_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Check whether email already exists
    is_email = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    if is_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash the password
    hashed = get_password_hash(body.password)

    # Create new user
    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hashed,
        email=body.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    bg_task.add_task(send_emails, [new_user.email])

    return new_user


def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(
        UserModel.username == body.username
    ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Username")

    if not verify_password(body.password, user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password")

    exp_time = datetime.now(timezone.utc) + timedelta(minutes=settings.EXP_TIME)

    token = jwt.encode(
        {"_id": user.id, "exp": exp_time},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"Token": token, "access_token": token, "token_type": "bearer"}


def is_authenticated(request: Request, db: Session):
    return helper_is_authenticated(request, db)
