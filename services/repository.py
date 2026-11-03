from services.database import get_connection

def salvar_ou_atualizar_filme(dados):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO filmes (imdb_id, titulo, ano, genero, diretor, elenco, sinopse, avaliacao_imdb, json_original, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(imdb_id) DO UPDATE SET
                titulo=excluded.titulo,
                ano=excluded.ano,
                genero=excluded.genero,
                diretor=excluded.diretor,
                elenco=excluded.elenco,
                sinopse=excluded.sinopse,
                avaliacao_imdb=excluded.avaliacao_imdb,
                json_original=excluded.json_original,
                atualizado_em=CURRENT_TIMESTAMP
        """, (
            dados.get("imdbID"), dados.get("Title"), dados.get("Year"),
            dados.get("Genre"), dados.get("Director"), dados.get("Actors"),
            dados.get("Plot"), dados.get("imdbRating"), dados.get("json_original")
        ))
        conn.commit()

def buscar_por_imdb_id(imdb_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM filmes WHERE imdb_id = ?", (imdb_id,)).fetchone()
        return dict(row) if row else None

def buscar_por_titulo(titulo):
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM filmes WHERE titulo LIKE ?", (f"%{titulo}%",)).fetchall()
        return [dict(r) for r in rows]

def listar_filmes():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM filmes ORDER BY atualizado_em DESC").fetchall()
        return [dict(r) for r in rows]