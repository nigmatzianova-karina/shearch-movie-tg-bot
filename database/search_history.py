import os
import sqlite3


class SearchHistory:
    def __init__(self, db_path='../data/search_history.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'search_history.db')
        self.conn = None
        self._create_table()

    def _create_table(self):
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = self.conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                user_id INTEGER,
                query TEXT,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
            if self.conn:
                self.conn.close()

    def add_record(self, user_id: int, query: str, result: str):
        try:
            if not self.conn:
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO search_history (user_id, query, result)
            VALUES (?, ?, ?)
            ''', (user_id, query, result))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")

    def get_history(self, user_id: int, limit: int = 10):
        try:
            if not self.conn:
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

            cursor = self.conn.cursor()
            cursor.execute('''
            SELECT query, result, timestamp 
            FROM search_history 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
            ''', (user_id, limit))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении истории: {e}")
            return []

    def clear_history(self, user_id: int):
        try:
            if not self.conn:
                self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM search_history WHERE user_id = ?', (user_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка при очистке истории: {e}")

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
