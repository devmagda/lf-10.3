import psycopg2

from app.config import Config

class Connection:
    def __init__(self, user, password, host, port, database):
        self.db = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

class ConnectionUtil:
    @staticmethod
    def from_global_config():
        return Connection(user=Config.DB_USER, password=Config.DB_PASSWORD, host=Config.DB_HOST, port=Config.DB_PORT, database=Config.DB_NAME)
