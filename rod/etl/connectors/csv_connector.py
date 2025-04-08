import logging
from pathlib import Path

import polars as pl
from django.conf import settings

from rod.etl.connectors.base_connector import BaseConnector
from rod.etl.connectors.connection_status_enum import ConnectionStatus

logger = logging.getLogger(__name__)


class CSVConnector(BaseConnector):
    def _resolve_path(self, url_path: str) -> Path:
        """
        Convert MEDIA_URL path to actual MEDIA_ROOT file path
        """
        if url_path.startswith(settings.MEDIA_URL):
            relative_path = url_path[len(settings.MEDIA_URL) :]
        else:
            relative_path = url_path
        return Path(settings.MEDIA_ROOT) / relative_path

    def check(self, config: dict) -> str:
        url_path = config.get("path")
        if not url_path:
            logger.warning("[CSVConnector] Check failed: missing 'path' in config")
            return ConnectionStatus.INVALID

        file_path = self._resolve_path(url_path)

        if not file_path.exists():
            logger.warning(
                "[CSVConnector] Check failed: file not found at %s",
                file_path,
            )
            return ConnectionStatus.INVALID

        try:
            logger.debug("[CSVConnector] Attempting to read CSV: %s", file_path)
            _ = pl.read_csv(file_path, n_rows=5)
            logger.info("[CSVConnector] Check valid for: %s", file_path)
            return ConnectionStatus.VALID  # noqa: TRY300
        except Exception:
            logger.exception("[CSVConnector] Failed to read CSV during check")
            return ConnectionStatus.INVALID

    def discover_schema(self, config: dict) -> dict:
        try:
            url_path = config["path"]
            file_path = self._resolve_path(url_path)
            logger.debug("[CSVConnector] Discovering schema for: %s", file_path)
        except KeyError:
            logger.warning("[CSVConnector] Missing 'path' in config: %s", config)
            return {
                "error": "Missing required config key: 'path'",
                "tables": {},
            }

        table_name = file_path.stem

        if not file_path.exists():
            logger.warning("[CSVConnector] File not found at: %s", file_path)
            return {
                "error": None,
                "tables": {
                    table_name: {
                        "error": f"File not found at path: {url_path}",
                        "columns": [],
                    },
                },
            }

        try:
            df = pl.read_csv(file_path, n_rows=100)  # noqa: PD901
            columns = [
                {"name": name, "dtype": str(dtype)}
                for name, dtype in zip(df.columns, df.dtypes, strict=False)
            ]
            logger.info(
                "[CSVConnector] Schema discovered for: %s -> %s",
                file_path,
                columns,
            )
            return {  # noqa: TRY300
                "error": None,
                "tables": {
                    table_name: {
                        "error": None,
                        "columns": columns,
                    },
                },
            }
        except Exception as e:
            logger.exception("[CSVConnector] Failed to read schema for %s", file_path)
            return {
                "error": None,
                "tables": {
                    table_name: {
                        "error": f"Failed to read schema: {e!s}",
                        "columns": [],
                    },
                },
            }
