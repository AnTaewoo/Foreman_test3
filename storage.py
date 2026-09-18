import sqlite3


class LinkStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS links (
                    code TEXT PRIMARY KEY,
                    url TEXT NOT NULL,
                    clicks INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            connection.commit()
        finally:
            connection.close()

    def save(self, code, url):
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "INSERT INTO links (code, url) VALUES (?, ?)",
                (code, url),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            raise KeyError(code) from None
        finally:
            connection.close()

    def get(self, code):
        connection = sqlite3.connect(self.db_path)
        try:
            row = connection.execute(
                "SELECT code, url, clicks FROM links WHERE code = ?",
                (code,),
            ).fetchone()
            if row is None:
                return None
            return {"code": row[0], "url": row[1], "clicks": row[2]}
        finally:
            connection.close()

    def increment_clicks(self, code):
        connection = sqlite3.connect(self.db_path)
        try:
            connection.execute(
                "UPDATE links SET clicks = clicks + 1 WHERE code = ?",
                (code,),
            )
            connection.commit()
        finally:
            connection.close()

    def list_all(self):
        connection = sqlite3.connect(self.db_path)
        try:
            rows = connection.execute(
                "SELECT code, url, clicks FROM links ORDER BY code"
            ).fetchall()
            return [
                {"code": row[0], "url": row[1], "clicks": row[2]}
                for row in rows
            ]
        finally:
            connection.close()
