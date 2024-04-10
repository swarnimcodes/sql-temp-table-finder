from asyncio import start_server
import sqlparse
from typing import Tuple


def format_sql(sql_content: str) -> Tuple[Exception | None, str | None]:
    try:
        formatted_sql: str = sqlparse.format(
            sql=sql_content,
            reindent=True,
            keyword_case='upper',
            strip_comments=True,
            comma_first=True,
            )
        return None, formatted_sql
    except Exception as e:
        return e, None
    
    
def split_sql(sql: str) -> Tuple[Exception | None, list[str] | None]:
    """ Only meant for formatted SQL Statements """
    try:
        sql_stmts: list[str] = sql.split('\n')
        return None, sql_stmts
    except Exception as e:
        return e, None
    
    
def syntax_sql(sql: str):
    try:
        parsed_syntax = sqlparse.parse(sql)
        return None, parsed_syntax
    except Exception as e:
        return e, None
    
# def has_temp_tables(sql: str):
#     parsed = sqlparse.parse(sql)
#     for stmt in parsed:
#         if any(token.normalized == "CREATE" and stmt.get_real_name() == "TEMP"
#                for token in stmt.tokens if token.ttype in (sqlparse.tokens.Keyword, sqlparse.tokens.DDL)):
#             return True
        
#     return False


def get_undropped_tables(formatted_sql: str) -> set[str]:
    created_temp_tables = set()
    dropped_temp_tables = set()

    split_sql = formatted_sql.split("\n")
    split_sql_iterator = iter(split_sql)

    for stmt in split_sql_iterator:
        if stmt.strip().upper().startswith("CREATE TABLE #"):
            tokens = stmt.split()
            for elem in tokens:
                if elem.startswith("#"):
                    comma_split = elem.split(",")
                    for element in comma_split:
                        bracket_split = element.split("(")
                        for item in bracket_split:
                            if item.startswith("#"):
                                created_temp_tables.add(item)
        elif stmt.strip().upper().startswith("INSERT"):
            tokens = stmt.split()
            # print(tokens)
            for elem in tokens:
                if elem.startswith("#"):
                    comma_split = elem.split(",")
                    for element in comma_split:
                        bracket_split = element.split("(")
                        for item in bracket_split:
                            if item.startswith("#"):
                                created_temp_tables.add(item)
        elif stmt.strip().upper().startswith("DROP TABLE"):
            tokens = stmt.split()
            # print(tokens)
            for elem in tokens:
                if elem.startswith("#"):
                    comma_split = elem.split(",")
                    for element in comma_split:
                        if element.startswith("#"):
                            dropped_temp_tables.add(element)
            next_line = next(split_sql_iterator, None)                            
            while next_line is not None and (next_line.strip().startswith(",") or next_line.strip().startswith("DROP")):
                tokens = next_line.split()
                # print(tokens)
                for elem in tokens:
                    if elem.startswith("#"):
                        comma_split = elem.split(",")
                        for element in comma_split:
                            if element.startswith("#"):
                                dropped_temp_tables.add(element)
                next_line = next(split_sql_iterator, None)

    for elem in dropped_temp_tables:
        if elem in created_temp_tables:
            created_temp_tables.remove(elem)
    
    return created_temp_tables
