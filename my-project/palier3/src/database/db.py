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
                    titre TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    tag TEXT,
                    image_ascii TEXT,
                    contenu TEXT
                )
            ''')
            conn.commit()
            
    def ajouter_livre(self, livre):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livres (titre, auteur, tag, image_ascii, contenu)
                VALUES (?, ?, ?, ?, ?)
            ''', (livre['titre'], livre['auteur'], livre['tag'], 
                 livre['image_ascii'], livre.get('contenu')))
            conn.commit()
            return True
            
    def supprimer_livre(self, titre, auteur):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM livres WHERE titre = ? AND auteur = ?
            ''', (titre, auteur))
            return cursor.rowcount > 0
            
    def liste_livres(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT titre, auteur, tag, image_ascii FROM livres')
            livres = []
            for row in cursor.fetchall():
                livres.append({
                    'titre': row[0],
                    'auteur': row[1],
                    'tag': row[2],
                    'image_ascii': row[3]
                })
            return livres