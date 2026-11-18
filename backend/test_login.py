from database import SessionLocal
from models import User
from security import verify_password, create_access_token

db = SessionLocal()
email = "admin@test.com"
password = "password123"

user = db.query(User).filter(User.email == email).first()
print("User ditemukan:", user is not None)
print("Awalan hash:", user.password_hash[:4], "| panjang:", len(user.password_hash))
print("Password cocok:", verify_password(password, user.password_hash))
print("Peran:", user.role.role_name)
print("Token:", create_access_token(user.user_id, user.role.role_name)[:20])