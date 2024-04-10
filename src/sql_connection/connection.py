import pyodbc
from pyodbc import Connection
from typing import Tuple


def get_connection(
    server: str,
    database: str,
    username: str,
    password: str,
    driver: str = "SQL Server",
) -> Tuple[Exception | None, Connection | None]:
    try:
        connection_string: str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        connection: Connection = pyodbc.connect(connection_string)
        return None, connection
    except Exception as err:
        return err, None
