from pyodbc import Connection
from typing import Tuple


def fetch_sp_names(connection: Connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE'
        """
        cursor.execute(query)
        sp_names: list[str] = []
        for sp in cursor.fetchall():
            sp_names.append(sp[0])
        return None, sp_names
    except Exception as e:
        return e, None


def fetch_sp_content(connection: Connection, sp_name: str) -> Tuple[Exception | None, str | None]:
    try:
        content: str = ""
        cursor = connection.cursor()
        query = f"""
            SELECT ROUTINE_DEFINITION
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_NAME = '{sp_name}'
            AND ROUTINE_TYPE = 'PROCEDURE'
        """
        cursor.execute(query)
        definition = cursor.fetchone()
        content = definition[0]
        cursor.close()
        return None, content
    except Exception as e:
        return e, None
