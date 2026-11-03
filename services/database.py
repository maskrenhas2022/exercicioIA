import sqlite3
import os

DB_PATH = os.path.join("data", "cineia.db")

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                imdb_id TEXT UNIQUE NOT NULL,
                titulo TEXT,
                ano TEXT,
                genero TEXT,
                diretor TEXT,
                elenco TEXT,
                sinopse TEXT,
                avaliacao_imdb TEXT,
                json_original TEXT,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()