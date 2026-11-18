import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import User, RevokedToken
from security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token tidak valid atau kedaluwarsa")

    if db.get(RevokedToken, payload["jti"]):
        raise HTTPException(status_code=401, detail="Token sudah logout")

    user = db.get(User, payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")
    return user

def require_roles(*allowed_roles: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role.role_name not in allowed_roles:
            raise HTTPException(status_code=403, detail="Peran kamu tidak punya akses ke fitur ini")
        return user
    return checker