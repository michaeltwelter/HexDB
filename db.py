import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS hexies (id INTEGER PRIMARY KEY, description TEXT, color_name TEXT, color_family TEXT, color_css TEXT, file_path TEXT)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT id, description, color_name, color_family FROM hexies")
        rows = self.cur.fetchall()
        return rows

    def load(self, id):
        self.cur.execute('SELECT id, description, color_name, color_family, color_css, file_path FROM hexies WHERE id=?', (id,))
        row = self.cur.fetchone()
        return row

    def insert(self, description, color_name, color_family, color_css, file_path):
        self.cur.execute('INSERT INTO hexies VALUES (NULL, ?, ?, ?, ?, ?)', (description, color_name, color_family, color_css, file_path))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute('DELETE FROM hexies WHERE id=?', (id,))
        self.conn.commit()

    def update(self, id, description, color_name, color_family):
        self.cur.execute('UPDATE hexies SET description = ?, color_name =?, color_camily = ? WHERE id = ?', (description, color_name, color_family, id))
        self.conn.commit()

    def get_max_index(self):
        self.cur.execute('SELECT MAX(id) FROM hexies')
        row = self.cur.fetchone()
        return row

    def __del__(self):
        self.conn.close()