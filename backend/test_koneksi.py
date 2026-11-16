from database import engine

try:
    engine.connect()
    print("OK, koneksi berhasil")
except Exception as e:
    print(type(e).__name__)
    print(str(e)[:400])