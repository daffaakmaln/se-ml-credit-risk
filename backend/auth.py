from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Role, RevokedToken
from security import hash_password, verify_password, create_access_token, decode_token
from deps import oauth2_scheme, get_current_user, require_roles
from utils import generate_id

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterIn(BaseModel):
    full_name: str
    email: str
    password: str

class RoleUpdateIn(BaseModel):
    role_name: str   # admin / credit_analyst / user

@router.post("/register", status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    email = data.email.strip().lower()
    if len(data.password) < 8 or len(data.password) > 72:
        raise HTTPException(400, "Password harus 8-72 karakter")
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email sudah terdaftar")

    role = db.query(Role).filter(Role.role_name == "user").first()
    user = User(
        user_id=generate_id(db, User.user_id, "U"),
        full_name=data.full_name,
        email=email,
        password_hash=hash_password(data.password),
        role_id=role.role_id,
    )
    db.add(user)
    db.commit()
    return {"message": "Registrasi berhasil", "user_id": user.user_id, "role": role.role_name}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username.strip().lower()).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Email atau password salah")
    token = create_access_token(user.user_id, user.role.role_name)
    return {"access_token": token, "token_type": "bearer", "role": user.role.role_name}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme),
           user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    payload = decode_token(token)
    expires = datetime.fromtimestamp(payload["exp"], timezone.utc).replace(tzinfo=None)
    db.add(RevokedToken(jti=payload["jti"], expires_at=expires))
    db.commit()
    return {"message": "Logout berhasil"}

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"user_id": user.user_id, "full_name": user.full_name,
            "email": user.email, "role": user.role.role_name}

# --- khusus Admin ---
@router.get("/users")
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    users = db.query(User).all()
    return [{"user_id": u.user_id, "email": u.email, "role": u.role.role_name} for u in users]

@router.put("/users/{user_id}/role")
def update_role(user_id: str, data: RoleUpdateIn,
                db: Session = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    user = db.get(User, user_id)
    role = db.query(Role).filter(Role.role_name == data.role_name).first()
    if not user or not role:
        raise HTTPException(404, "User atau peran tidak ditemukan")
    user.role_id = role.role_id
    db.commit()
    return {"message": f"Peran {user.email} diubah ke {role.role_name}"}