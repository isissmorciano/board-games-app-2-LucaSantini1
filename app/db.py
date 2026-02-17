import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'board_games.db')

def init_db():
    # Ensure database file exists and seed initial data if missing
    db_path = os.path.abspath(DATABASE)
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS giochi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero_giocatori_massimo INTEGER NOT NULL,
            durata_media INTEGER NOT NULL,
            categoria TEXT NOT NULL
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS partite (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gioco_id INTEGER NOT NULL,
            data DATE NOT NULL,
            vincitore TEXT NOT NULL,
            punteggio_vincitore INTEGER NOT NULL,
            FOREIGN KEY (gioco_id) REFERENCES giochi (id)
        )''')

        # Seed example data
        c.executemany('INSERT INTO giochi (nome, numero_giocatori_massimo, durata_media, categoria) VALUES (?, ?, ?, ?)', [
            ('Catan', 4, 90, 'Strategia'),
            ('Dixit', 6, 30, 'Party'),
            ('Ticket to Ride', 5, 60, 'Strategia')
        ])

        c.executemany('INSERT INTO partite (gioco_id, data, vincitore, punteggio_vincitore) VALUES (?, ?, ?, ?)', [
            (1, '2023-10-15', 'Alice', 10),
            (1, '2023-10-22', 'Bob', 12),
            (2, '2023-11-05', 'Charlie', 25),
            (3, '2023-11-10', 'Alice', 8)
        ])

        conn.commit()
        conn.close()


def get_db():
    conn = sqlite3.connect(os.path.abspath(DATABASE))
    conn.row_factory = sqlite3.Row
    return conn
