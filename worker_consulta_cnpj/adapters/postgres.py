import psycopg2


class PostgresAdapter:
    def __init__(self, host, db, username, password, port):
        self.host = host
        self.db = db
        self.username = username
        self.password = password
        self.port = port
        self.cur = None
        self.conn = None

    def connect(self):
        # self.conn = psycopg2.connect(dsn)
        self.conn = psycopg2.connect(
            database=self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )

        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def commit(self):
        self.conn.commit()
