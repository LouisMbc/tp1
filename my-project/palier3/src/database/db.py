import sqlite3

class BiblioDatabase:
    def __init__(self, db_file="bibliotheque.db"):
        self.db_file = db_file
        self.init_db()
        
    def init_db(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS livres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    tag TEXT,
                    image_ascii TEXT,
                    content TEXT
                )
            ''')
            conn.commit()
            
    def ajouter_livre(self, livre):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livres (title, author, tag, image_ascii, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (livre['title'], livre['author'], livre['tag'], 
                 livre['image_ascii'], livre.get('content')))
            conn.commit()
            return True
            
    def supprimer_livre(self, title, author):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM livres WHERE title = ? AND author = ?
            ''', (title, author))
            return cursor.rowcount > 0
            
    def liste_livres(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, author, tag, image_ascii, content FROM livres')
            livres = []
            for row in cursor.fetchall():
                livres.append({
                    'id': row[0],
                    'title': row[1],
                    'author': row[2],
                    'tag': row[3],
                    'image_ascii': row[4],
                    'content': row[5]
                })
            return livres