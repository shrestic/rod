import logging

import polars as pl
from sqlalchemy import create_engine
from sqlalchemy import text

from rod.etl.connectors.base_connector import BaseConnector
from rod.etl.connectors.connection_status_enum import ConnectionStatus

logger = logging.getLogger(__name__)


class SQLServerConnector(BaseConnector):
    def _get_engine(self, config: dict):
        required_keys = {"user", "password", "host", "db_name"}
        missing_keys = required_keys - config.keys()
        if missing_keys:
            msg = f"Missing required DB config: {', '.join(missing_keys)}"
            raise ValueError(msg)

        try:
            user = config["user"]
            password = config["password"]
            host = config["host"]
            port = config.get("port", 1433)  # Default SQL Server port
            db_name = config["db_name"]
            connection_string = (
                f"mssql+pymssql://{user}:{password}@{host}:{port}/{db_name}"
            )

            return process_create_engine(connection_string)
        except Exception as e:
            logger.exception("[SQLServerConnector] Failed to create engine")
            msg = f"Invalid database configuration: {e}"
            raise ValueError(msg)  # noqa: B904

    def check(self, config: dict) -> str:
        try:
            engine = self._get_engine(config)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            return ConnectionStatus.VALID  # noqa: TRY300
        except Exception as e:
            logger.exception("[SQLServerConnector] Check failed: %s", e)  # noqa: TRY401
            return ConnectionStatus.INVALID

    def discover_schema(self, config: dict) -> dict:
        try:
            engine = self._get_engine(config)
            table_query = """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE';
            """
            tables_df = pl.read_database(query=table_query, connection=engine)

            logger.info("[SQLServerConnector] All tables: %d rows", tables_df.shape[0])

            if tables_df.is_empty():
                logger.warning(
                    "[SQLServerConnector] No base tables found in the database",
                )
                return {"error": None, "tables": {}}
            tables_df = tables_df.rename(
                {col: col.lower() for col in tables_df.columns},
            )

            db_schema = config.get("db_schema")
            if db_schema:
                tables_df = tables_df.filter(pl.col("table_schema") == db_schema)

            schema = {}

            for row in tables_df.to_dicts():
                schema_name = row["table_schema"]
                table_name = row["table_name"]
                full_table = f"{schema_name}.{table_name}"
                logger.info("Processing table: %s", full_table)

                try:
                    column_query = """
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_schema = :schema_name
                        AND table_name = :table_name
                    """
                    columns_df = pl.read_database(
                        query=column_query,
                        connection=engine,
                        execute_options={
                            "parameters": {
                                "schema_name": schema_name,
                                "table_name": table_name,
                            },
                        },
                    )

                    columns_df = columns_df.rename(
                        {col: col.lower() for col in columns_df.columns},
                    )

                    columns = [
                        {
                            "name": col["column_name"],
                            "dtype": col.get("data_type", "UNKNOWN"),
                        }
                        for col in columns_df.to_dicts()
                    ]
                    schema[full_table] = {"error": None, "columns": columns}
                except Exception as e:
                    logger.exception(
                        "[SQLServerConnector] Failed reading table: %s",
                        full_table,
                    )
                    schema[full_table] = {"error": str(e), "columns": []}

            return {"error": None, "tables": schema}  # noqa: TRY300

        except Exception as e:
            logger.exception("[SQLServerConnector] Failed to discover schema")
            return {"error": f"Failed to discover schema: {e!s}", "tables": {}}


def process_create_engine(connection_string):
    return create_engine(connection_string)
