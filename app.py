import streamlit as st
from services.database import init_db
from services.repository import buscar_por_imdb_id, buscar_por_titulo, salvar_ou_atualizar_filme, listar_filmes
from services.omdb_api import buscar_filme_omdb
from services.ia_service import perguntar_ia

# Inicializa o banco na primeira execução
init_db()

st.title("🎬 CineIA com SQLite")

# --- Sidebar: Catálogo Local ---
with st.sidebar:
    st.header("Catálogo Local (SQLite)")
    filmes_salvos = listar_filmes()
    if filmes_salvos:
        for f in filmes_salvos:
            st.write(f"**{f['titulo']}** ({f['ano']}) - IMDb: {f['avaliacao_imdb']}")
    else:
        st.write("Nenhum filme salvo ainda.")

# --- Aba Principal: Busca ---
st.subheader("Buscar Filme")
titulo_busca = st.text_input("Digite o título do filme:")

if st.button("Buscar"):
    # 1. Tenta buscar no SQLite primeiro (busca simples por título)
    resultados_locais = buscar_por_titulo(titulo_busca)
    if resultados_locais:
        st.info(f"Encontrado no SQLite (Cache).")
        filme = resultados_locais[0] # Pega o primeiro resultado
    else:
        # 2. Se não achar, busca na OMDb
        st.info("Buscando na OMDb...")
        dados_omdb = buscar_filme_omdb(titulo_busca)
        if "erro" in dados_omdb:
            st.error(dados_omdb["erro"])
            filme = None
        else:
            # Salva no SQLite
            salvar_ou_atualizar_filme(dados_omdb)
            st.success("Filme salvo/atualizado no banco local!")
            filme = buscar_por_imdb_id(dados_omdb.get("imdbID")) # Recupera do banco para padronizar

    if filme:
        st.write(f"### {filme['titulo']} ({filme['ano']})")
        st.write(f"**Diretor:** {filme['diretor']}")
        st.write(f"**Elenco:** {filme['elenco']}")
        st.write(f"**Sinopse:** {filme['sinopse']}")
        
        # --- Seção de Perguntas para a IA ---
        st.divider()
        st.subheader("Pergunte à IA sobre este filme")
        pergunta = st.text_input("Sua pergunta:", key="pergunta_ia")
        if st.button("Perguntar"):
            with st.spinner("Consultando IA local..."):
                resposta = perguntar_ia(pergunta, filme)
                st.write("**Resposta da IA:**")
                st.write(resposta)