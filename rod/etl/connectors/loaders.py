from rod.etl.connectors.csv_connector import CSVConnector
from rod.etl.connectors.excel_connector import ExcelConnector
from rod.etl.connectors.json_connector import JsonConnector
from rod.etl.connectors.mssql_connector import SQLServerConnector
from rod.etl.connectors.mysql_connector import MySQLConnector
from rod.etl.connectors.postgres_connector import PostgreSQLConnector
from rod.etl.connectors.sqlite_connector import SQLiteConnector

CONNECTOR_MAP = {
    "csv": CSVConnector,
    "xlsx": ExcelConnector,
    "json": JsonConnector,
    "sqlite": SQLiteConnector,
    "postgres": PostgreSQLConnector,
    "mysql": MySQLConnector,
    "mssql": SQLServerConnector,
}


def get_connector_class(code: str):
    return CONNECTOR_MAP[code]
