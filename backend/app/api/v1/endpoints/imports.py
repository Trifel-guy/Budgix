from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.services.import_service import parse_transactions_file

router = APIRouter(prefix="/import", tags=["import"])

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@router.post("/transactions")
async def import_transactions(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in (
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    ):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are accepted")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 5 MB)")

    try:
        result = parse_transactions_file(content, file.filename, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return result


@router.get("/template")
def download_template():
    """Return CSV template headers."""
    return {
        "columns": ["date", "amount", "type", "description", "category", "tags", "note"],
        "example": {
            "date": "2024-01-15",
            "amount": "49.99",
            "type": "expense",
            "description": "Supermarché",
            "category": "Alimentation",
            "tags": "courses, quotidien",
            "note": "Carrefour",
        },
    }
