import os
from database import SessionLocal, Report

STORAGE_DIR = "storage"


def save_report_for_user(user_id: int, pdf_path: str):
    os.makedirs(STORAGE_DIR, exist_ok=True)

    user_folder = os.path.join(STORAGE_DIR, f"user_{user_id}")
    os.makedirs(user_folder, exist_ok=True)

    filename = os.path.basename(pdf_path)
    new_path = os.path.join(user_folder, filename)

    os.replace(pdf_path, new_path)

    db = SessionLocal()
    report = Report(user_id=user_id, file_path=new_path)
    db.add(report)
    db.commit()
    db.close()

    return new_path


def get_user_reports(user_id: int):
    db = SessionLocal()

    reports = (
        db.query(Report)
        .filter(Report.user_id == user_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    db.close()

    return [r.file_path for r in reports]