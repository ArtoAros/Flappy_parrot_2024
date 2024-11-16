# database.py

import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, db_path: str = 'highscores.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Создает таблицу для хранения рекордов, если она еще не существует."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS highscores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')
        self.connection.commit()

    def save_score(self, name: str, score: int):
        """Сохраняет новый рекорд в базу данных."""
        self.cursor.execute('''
            INSERT INTO highscores (name, score)
            VALUES (?, ?)
        ''', (name, score))
        self.connection.commit()

    def get_high_scores(self, limit: int = 3) -> List[Tuple[str, int]]:
        """Возвращает список лучших рекордов, отсортированных по убыванию."""
        self.cursor.execute('''
            SELECT name, score FROM highscores
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()

    def __del__(self):
        self.close()
