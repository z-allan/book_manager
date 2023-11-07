from services.sqlite_db import SQLiteDatabaseConnection
from datetime import datetime
import pytz

class DatabaseConnection:

    instance = None

    def __new__(cls, close=False):
        hora = datetime.now().astimezone(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
        if close:
            if cls.instance is not None:
                print(f'[{hora}] closing connection')
                cls.instance = None
            return
        if cls.instance is None:
            print(f'[{hora}] creating new instance (in file)')
            cls.instance = SQLiteDatabaseConnection()
        return cls.instance
