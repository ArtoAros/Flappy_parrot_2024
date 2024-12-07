import sqlite3

class Database:
    def __init__(self, db_name='scores.db'):
        # Подключаемся к базе данных (если ее нет - будет создана)
        self.conn = sqlite3.connect(db_name)
        # Создаем таблицу, если она еще не существует
        self.conn.execute('''CREATE TABLE IF NOT EXISTS scores (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                score INTEGER NOT NULL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                             )''')
        self.conn.commit()

    def add_score(self, score):
        # Добавляем запись с результатом в таблицу
        self.conn.execute('INSERT INTO scores (score) VALUES (?)', (score,))
        self.conn.commit()

    def get_top_scores(self, limit=5):
        # Получаем top N результатов по убыванию
        cur = self.conn.execute('SELECT score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
        return [row[0] for row in cur.fetchall()]

    def close(self):
        self.conn.close()
