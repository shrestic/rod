import logging

import polars as pl
from sqlalchemy import create_engine
from sqlalchemy import text

from rod.etl.connectors.base_connector import BaseConnector
from rod.etl.connectors.connection_status_enum import ConnectionStatus

logger = logging.getLogger(__name__)


class MySQLConnector(BaseConnector):
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
            port = config.get("port", 3306)
            db_name = config["db_name"]
            return create_engine(
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}",
            )
        except Exception as e:
            logger.exception("[MySQLConnector] Failed to create engine")
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
            logger.exception("[MySQLConnector] Check failed: %s", e)  # noqa: TRY401
            return ConnectionStatus.INVALID

    def discover_schema(self, config: dict) -> dict:
        try:
            engine = self._get_engine(config)

            # Query to fetch tables
            table_query = """
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_type = 'BASE TABLE'
                AND table_schema = :db_name;
            """
            tables_df = pl.read_database(
                query=table_query,
                connection=engine,
                execute_options={"parameters": {"db_name": config["db_name"]}},
            )
            logger.info("Tables DataFrame: %s", tables_df)
            logger.info("Columns in DataFrame: %s", tables_df.columns)

            schema = {}
            if tables_df.is_empty():
                logger.info("No tables found for database: %s", config["db_name"])
                return {"error": None, "tables": schema}

            # Normalize column names to lowercase
            tables_df = tables_df.rename(
                {col: col.lower() for col in tables_df.columns},
            )

            for row in tables_df.to_dicts():
                schema_name = row.get("table_schema")
                table_name = row.get("table_name")
                if not schema_name or not table_name:
                    logger.error("Missing expected columns in row: %s", row)
                    continue

                full_table = f"{schema_name}.{table_name}"
                logger.info("Processing table: %s", full_table)

                try:
                    # Use parameterized query for column information
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
                    logger.info("Columns DataFrame for %s: %s", full_table, columns_df)
                    logger.info("Columns in DataFrame: %s", columns_df.columns)

                    if columns_df.is_empty():
                        logger.info("No columns found for table: %s", full_table)
                        schema[full_table] = {
                            "error": "No columns found",
                            "columns": [],
                        }
                        continue

                    # Normalize column names to lowercase
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
                        "[MySQLConnector] Failed reading table: %s",
                        full_table,
                    )
                    schema[full_table] = {"error": str(e), "columns": []}

            return {"error": None, "tables": schema}  # noqa: TRY300

        except Exception as e:
            logger.exception("[MySQLConnector] Failed to discover schema")
            return {"error": f"Failed to discover schema: {e!s}", "tables": {}}
