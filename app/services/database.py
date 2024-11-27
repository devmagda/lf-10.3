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
        # Extract each variable from the Config class
        user = Config.DB_USER
        password = Config.DB_PASSWORD
        host = Config.DB_HOST
        port = Config.DB_PORT
        database = Config.DB_NAME

        # Print each variable
        print(f"DB_USER: {user}")
        print(f"DB_PASSWORD: {password}")
        print(f"DB_HOST: {host}")
        print(f"DB_PORT: {port}")
        print(f"DB_NAME: {database}")

        # Create and return the Connection object
        return Connection(user=user, password=password, host=host, port=port, database=database)
