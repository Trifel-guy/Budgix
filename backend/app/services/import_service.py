from io import BytesIO
from datetime import date
from decimal import Decimal, InvalidOperation

import pandas as pd
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType
from app.models.category import Category


REQUIRED_COLUMNS = {"amount", "type", "description", "date"}

COLUMN_ALIASES = {
    "montant": "amount",
    "type": "type",
    "libelle": "description",
    "description": "description",
    "note": "note",
    "date": "date",
    "tags": "tags",
    "categorie": "category",
    "category": "category",
}


def parse_transactions_file(
    content: bytes,
    filename: str,
    user_id,
    db: Session,
) -> dict:
    """Parse CSV or Excel file and bulk-insert transactions."""
    if not filename:
        raise ValueError("Filename is required to detect file format.")
    if filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(content))
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(BytesIO(content))
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    # Normalize column names
    df.columns = [COLUMN_ALIASES.get(c.lower().strip(), c.lower().strip()) for c in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Load user categories for matching
    categories = {c.name.lower(): c.id for c in db.query(Category).filter(Category.user_id == user_id).all()}

    created, errors = [], []

    for idx, row in df.iterrows():
        try:
            amount = Decimal(str(row["amount"])).quantize(Decimal("0.01"))
            if amount <= 0:
                raise ValueError("Amount must be positive")

            tx_type = str(row["type"]).lower().strip()
            if tx_type not in ("income", "expense"):
                raise ValueError(f"Invalid type: {tx_type}")

            tx_date = pd.to_datetime(row["date"]).date()

            category_id = None
            if "category" in row and pd.notna(row["category"]):
                category_id = categories.get(str(row["category"]).lower().strip())

            tags = []
            if "tags" in row and pd.notna(row["tags"]):
                tags = [t.strip() for t in str(row["tags"]).split(",") if t.strip()]

            tx = Transaction(
                user_id=user_id,
                amount=amount,
                type=TransactionType(tx_type),
                description=str(row["description"])[:255],
                note=str(row["note"]) if "note" in row and pd.notna(row.get("note")) else None,
                date=tx_date,
                tags=tags,
                category_id=category_id,
            )
            db.add(tx)
            created.append(idx)
        except (ValueError, InvalidOperation, Exception) as e:
            errors.append({"row": idx + 2, "error": str(e)})

    db.commit()
    return {"created": len(created), "errors": errors}
