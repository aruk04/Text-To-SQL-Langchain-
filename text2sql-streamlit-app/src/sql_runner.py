import os
from sqlalchemy import create_engine, text

# Read DB URI from environment (common names). Provide clear error if missing.
DATABASE_URI = os.environ.get("DB_URI") or os.environ.get("DATABASE_URI")
if not DATABASE_URI:
    raise RuntimeError(
        "Database URI not set. Set DB_URI (or DATABASE_URI) environment variable.\n"
        'Example (PowerShell): $env:DB_URI = "mysql+pymysql://root:arushisql@localhost:3306/text_to_sql"'
    )

engine = create_engine(DATABASE_URI, future=True)


def execute_query(query: str):
    """
    Execute a SQL query and return results as list[dict] when possible.
    Raises exceptions from SQLAlchemy on error.
    """
    if not query:
        raise ValueError("No query provided to execute_query.")

    with engine.connect() as conn:
        result = conn.execute(text(query))
        try:
            # SQLAlchemy 1.4+ RowMapping support
            rows = [dict(row) for row in result.mappings().all()]
            return rows
        except Exception:
            # fallback for older/result types
            try:
                return [tuple(row) for row in result.fetchall()]
            except Exception:
                return []