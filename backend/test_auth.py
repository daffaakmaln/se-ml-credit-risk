from security import SECRET_KEY, create_access_token
from database import SessionLocal
from models import User

print("SECRET_KEY terisi:", bool(SECRET_KEY))

db = SessionLocal()
print("Daftar user:", [(u.email, u.role.role_name) for u in db.query(User).all()])

print("Token berhasil dibuat:", create_access_token("U0001", "user")[:20], "...")