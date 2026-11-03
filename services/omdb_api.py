import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

def buscar_filme_omdb(titulo):
    if not API_KEY or API_KEY == "sua_chave_aqui":
        return {"erro": "Chave da OMDb não configurada no .env"}
    
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={titulo}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        
        if dados.get("Response") == "False":
            return {"erro": dados.get("Error", "Filme não encontrado.")}
        
        dados["json_original"] = response.text
        return dados
    except requests.exceptions.RequestException as e:
        return {"erro": f"Falha de rede: {e}"}