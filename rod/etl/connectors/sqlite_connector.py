import logging
from pathlib import Path

import polars as pl
from django.conf import settings
from sqlalchemy import create_engine
from sqlalchemy import text

from rod.etl.connectors.base_connector import BaseConnector
from rod.etl.connectors.connection_status_enum import ConnectionStatus

logger = logging.getLogger(__name__)


class SQLiteConnector(BaseConnector):
    def _resolve_path(self, db_path: str) -> Path:
        """
        Convert MEDIA_URL path to actual MEDIA_ROOT file path.
        Ensures the path is safe and valid.
        """
        if not db_path or not isinstance(db_path, str):
            msg = "Invalid or empty database path"
            raise ValueError(msg)

        if db_path.startswith(settings.MEDIA_URL):
            relative_path = db_path[len(settings.MEDIA_URL) :]
        else:
            relative_path = db_path

        # Construct the full path
        full_path = Path(settings.MEDIA_ROOT) / relative_path

        # Basic path validation to prevent directory traversal
        try:
            full_path.resolve().relative_to(Path(settings.MEDIA_ROOT).resolve())
        except ValueError:
            logger.warning("[SQLiteConnector] Invalid path detected: %s", full_path)
            raise ValueError("Path is outside of allowed directory")  # noqa: B904, EM101, TRY003

        return full_path

    def _get_engine(self, db_path: Path):
        return create_engine(f"sqlite:///{db_path}")

    def check(self, config: dict) -> str:
        db_path = config.get("path")
        if not db_path:
            logger.warning("[SQLiteConnector] Missing DB path in config")
            return ConnectionStatus.INVALID

        try:
            db_path = self._resolve_path(db_path)
        except ValueError as e:
            logger.warning("[SQLiteConnector] Path resolution failed: %s", e)
            return ConnectionStatus.INVALID

        if not db_path.exists():
            logger.warning("[SQLiteConnector] DB path not found: %s", db_path)
            return ConnectionStatus.INVALID

        try:
            engine = self._get_engine(db_path)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return ConnectionStatus.VALID  # noqa: TRY300
        except Exception as e:
            logger.exception("[SQLiteConnector] Check failed: %s", e)  # noqa: TRY401
            return ConnectionStatus.INVALID

    def discover_schema(self, config: dict) -> dict:
        db_path = config.get("path")
        if not db_path:
            logger.warning("[SQLiteConnector] Missing DB path in config")
            return {"error": "Missing DB path", "tables": {}}

        try:
            db_path = self._resolve_path(db_path)
        except ValueError as e:
            logger.warning("[SQLiteConnector] Path resolution failed: %s", e)
            return {"error": str(e), "tables": {}}

        if not db_path.exists():
            logger.warning("[SQLiteConnector] DB path not found: %s", db_path)
            return {"error": "DB file not found", "tables": {}}

        try:
            engine = self._get_engine(db_path)
            schema = {}

            # Get list of tables
            table_query = """
                SELECT name AS table_name
                FROM sqlite_master
                WHERE type = 'table';
            """
            tables_df = pl.read_database(table_query, connection=engine)

            # Iterate through each table to get schema
            for table_name in tables_df["table_name"]:
                try:
                    # Use PRAGMA table_info to get column information
                    query = f'PRAGMA table_info("{table_name}")'
                    columns_df = pl.read_database(query, connection=engine)

                    columns = [
                        {
                            "name": row["name"],
                            "dtype": row["type"]
                            or "UNKNOWN",  # SQLite type or fallback
                        }
                        for row in columns_df.to_dicts()
                    ]
                    schema[table_name] = {"error": None, "columns": columns}
                except Exception as e:
                    logger.exception(
                        "[SQLiteConnector] Error reading table: %s",
                        table_name,
                    )
                    schema[table_name] = {"error": str(e), "columns": []}

            return {"error": None, "tables": schema}  # noqa: TRY300

        except Exception as e:
            logger.exception("[SQLiteConnector] Failed discover_schema: %s", e)  # noqa: TRY401
            return {"error": f"Failed to discover schema: {e!s}", "tables": {}}
