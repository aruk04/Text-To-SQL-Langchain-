import os
from typing import Optional
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

_engine: Optional[Engine] = None

def _get_database_uri() -> Optional[str]:
    return os.environ.get("DB_URI") or os.environ.get("DATABASE_URI")

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        db_uri = _get_database_uri()
        if not db_uri:
            raise RuntimeError(
                "Database URI not set. Set DB_URI (or DATABASE_URI) environment variable.\n"
                'Example (PowerShell): $env:DB_URI = "mysql+pymysql://root:arushisql@localhost:3306/text_to_sql"'
            )
        _engine = create_engine(db_uri, future=True)
    return _engine

def get_schema() -> str:
    """
    Return a readable schema string (table list + columns). Raises RuntimeError if DB_URI missing.
    """
    engine = get_engine()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    parts = []
    for t in tables:
        cols = inspector.get_columns(t)
        col_lines = [f"  - {c['name']} ({c.get('type')})" for c in cols]
        parts.append(f"Table: {t}\n" + "\n".join(col_lines))
    return "\n\n".join(parts)

def run_sql(query: str):
    """
    Execute query and return list[dict] when possible.
    """
    if not query:
        return []
    engine = get_engine()
    with engine.connect() as conn:
        res = conn.execute(text(query))
        try:
            return [dict(r) for r in res.mappings().all()]
        except Exception:
            return [tuple(r) for r in res.fetchall()]