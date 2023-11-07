import sqlite3
from streamlit import secrets

class SQLiteDatabaseConnection:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(SQLiteDatabaseConnection, cls).__new__(cls)
            cls.instance.connection = sqlite3.connect(secrets.sqlite.db_name, check_same_thread=False)
            cls.instance.connection.execute("PRAGMA foreign_keys = 1")
            return cls.instance
        return cls.instance

    def search(self, sql, params=()):
        try:
            resp = self.connection.execute(sql, params).fetchall()
            return resp
        finally:
            self.connection.cursor().close()
    
    def change(self, sql, params=()):
        try:
            self.connection.execute(sql, params)
            self.connection.commit()
            resp = self.connection.execute('select last_insert_rowid()').fetchone()[0]
            return resp
        except Exception:
            raise Exception
        finally:
            self.connection.cursor().close()
    
        

