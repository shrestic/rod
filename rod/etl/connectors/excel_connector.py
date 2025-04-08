import logging
from pathlib import Path

import pandas as pd
import polars as pl
from django.conf import settings

from rod.etl.connectors.base_connector import BaseConnector
from rod.etl.connectors.connection_status_enum import ConnectionStatus

logger = logging.getLogger(__name__)


class ExcelConnector(BaseConnector):
    def _resolve_path(self, url_path: str) -> Path:
        if url_path.startswith(settings.MEDIA_URL):
            relative_path = url_path[len(settings.MEDIA_URL) :]
        else:
            relative_path = url_path
        return Path(settings.MEDIA_ROOT) / relative_path

    def check(self, config: dict) -> str:
        url_path = config.get("path")
        if not url_path:
            logger.warning("[ExcelConnector] Check failed: missing 'path' in config")
            return ConnectionStatus.INVALID

        file_path = self._resolve_path(url_path)

        if not file_path.exists():
            logger.warning("[ExcelConnector] File not found at: %s", file_path)
            return ConnectionStatus.INVALID

        try:
            df = pd.read_excel(file_path, sheet_name=0, nrows=5)  # noqa: PD901
            _ = pl.from_pandas(df)
            logger.info("[ExcelConnector] Check valid for: %s", file_path)
            return ConnectionStatus.VALID  # noqa: TRY300
        except Exception as e:
            logger.exception(
                "[ExcelConnector] Failed to read Excel during check: %s",
                e,  # noqa: TRY401
            )
            return ConnectionStatus.INVALID

    def discover_schema(self, config: dict) -> dict:
        try:
            url_path = config["path"]
            file_path = self._resolve_path(url_path)
            logger.debug("[ExcelConnector] Resolving path for schema: %s", file_path)
        except KeyError:
            logger.warning("[ExcelConnector] Missing 'path' in config: %s", config)
            return {
                "error": "Missing required config key: 'path'",
                "tables": {},
            }

        if not file_path.exists():
            logger.warning("[ExcelConnector] File not found at: %s", file_path)
            return {
                "error": None,
                "tables": {
                    file_path.stem: {
                        "error": f"File not found at path: {url_path}",
                        "columns": [],
                    },
                },
            }

        try:
            sheet_dict = pd.read_excel(file_path, sheet_name=None)
            tables = {}

            for sheet_name, pd_df in sheet_dict.items():
                try:
                    df = pl.from_pandas(pd_df.head(100))  # noqa: PD901
                    columns = [
                        {"name": name, "dtype": str(dtype)}
                        for name, dtype in zip(
                            df.columns,
                            df.dtypes,
                            strict=False,
                        )
                    ]
                    logger.info(
                        "[ExcelConnector] Schema for sheet '%s': %s",
                        sheet_name,
                        columns,
                    )
                    tables[sheet_name] = {
                        "error": None,
                        "columns": columns,
                    }
                except Exception as e:
                    logger.exception(
                        "[ExcelConnector] Failed to read sheet: %s",
                        sheet_name,
                    )
                    tables[sheet_name] = {
                        "error": f"Failed to read sheet '{sheet_name}': {e!s}",
                        "columns": [],
                    }

            return {  # noqa: TRY300
                "error": None,
                "tables": tables,
            }

        except Exception as e:
            logger.exception("[ExcelConnector] Failed to discover schema")
            return {
                "error": f"Failed to discover schema: {e!s}",
                "tables": {},
            }
