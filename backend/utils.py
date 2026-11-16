from sqlalchemy import func

def generate_id(db, id_column, prefix):
    last = db.query(func.max(id_column)).scalar()
    num = int(last.strip()[1:]) + 1 if last else 1
    return f"{prefix}{num:04d}"