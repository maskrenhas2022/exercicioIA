import ollama
from services.prompts import SYSTEM_PROMPT

def perguntar_ia(pergunta, contexto_filme):
    # Formata o contexto para a IA ler
    contexto_texto = f"""
    Dados do filme:
    - Título: {contexto_filme.get('titulo')}
    - Ano: {contexto_filme.get('ano')}
    - Gênero: {contexto_filme.get('genero')}
    - Diretor: {contexto_filme.get('diretor')}
    - Elenco: {contexto_filme.get('elenco')}
    - Sinopse: {contexto_filme.get('sinopse')}
    - Avaliação IMDb: {contexto_filme.get('avaliacao_imdb')}
    """
    
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': f"Contexto: {contexto_texto}\n\nPergunta: {pergunta}"}
    ]
    
    try:
        response = ollama.chat(model='llama3.2', messages=messages) # Ajuste o modelo conforme o seu
        return response['message']['content']
    except Exception as e:
        return f"Erro ao contatar a IA local: {e}"