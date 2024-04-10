import datetime


def hello():
    print("Hello from custom logger!")


def log(log_level: int, message: str) -> None:
    log_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level: str = ""
    match log_level:
        case 1:
            level = "INFO"
        case 2:
            level = "ERROR"
        case 3:
            level = "EXCEPTION"
        case 4:
            level = "FATAL"
        case _:
            level = "INFO"
    print(f"[{log_datetime}] :: [{level}]  -->  [{message}]")
    return None
