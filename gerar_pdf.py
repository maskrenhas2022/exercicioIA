from fpdf import FPDF

# Cria o PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

texto = """
GUIA DIDATICO: COMO RESOLVER O EXERCICIO CINEIA (SQLITE + OLLAMA)
Objetivo: Explicar de forma simples como o codigo do projeto esta estruturado.

1. ENTENDENDO A ARQUITETURA DO PROJETO
O professor pediu um projeto modular. A estrutura do seu VS Code esta perfeita:
- app.py: A interface visual (Streamlit).
- services/omdb_api.py: Busca os dados na API do OMDb.
- services/database.py: Cria o banco SQLite e as tabelas.
- services/repository.py: Faz os comandos SQL (INSERT, SELECT, UPDATE).
- services/prompts.py: O system prompt da IA.
- services/ia_service.py: Comunica com o Ollama.

2. PASSO A PASSO DA SOLUCAO
Passo A: O Banco de Dados
- Criacao Automatica: O database.py verifica se o cineia.db existe.
- Evitando Duplicidade: O repository.py usa o imdb_id como chave unica. Se o ID existe, faz UPDATE. Se nao, faz INSERT.

Passo B: Buscando na Internet
- O omdb_api.py pega a chave do .env e faz a requisicao HTTP.
- Tratamento de Erros: Se a internet cair ou o filme nao existir, o app avisa o usuario.

Passo C: O Fluxo Inteligente (Cache vs API)
- O usuario pesquisa "O Exorcista".
- O app pergunta ao banco: "Ja temos esse filme?".
- Se sim: pega do SQLite e avisa "Dados recuperados do Banco Local".
- Se nao: chama a OMDb, salva no SQLite e avisa "Dados recuperados da Internet".

Passo D: A Inteligencia Artificial
- O prompts.py diz a IA: "Voce e o CineIA, so fala de terror, nao invente dados".
- O ia_service.py junta os dados do filme + a pergunta + o SYSTEM_PROMPT e envia para o Ollama.

3. COMO PASSAR NOS TESTES OBRIGATORIOS
1. Pesquisar filme novo: vai na OMDb e salva no SQLite.
2. Repetir pesquisa: puxa do SQLite (fonte Local). Sem duplicatas.
3. Desligar OMDb (sem wifi): pesquisa filme salvo e funciona.
4. Titulo inexistente: mostra mensagem amigavel.
5. Listar 5 filmes: botao na barra lateral le o SQLite.
6. Testar IA (Dados Reais): pergunta a sinopse, ela responde com base no banco.
7. Testar IA (Limitacao): pergunta a bilheteria (que nao esta no banco). Ela deve dizer "Nao tenho essa informacao".

4. DICAS PARA A ENTREGA
- Nao envie o .env (sua chave OMDb e pessoal). Crie um .env.example.
- O arquivo do Banco: pesquise 5 filmes antes de zipar e envie o cineia.db.
- README.md: escreva como rodar (pip install, ollama run, streamlit run).
"""

# Adiciona o texto ao PDF (com tratamento de quebra de linha e acentos)
for linha in texto.split('\n'):
    # O fpdf padrão tem problemas com acentos, então limpamos os caracteres
    linha_limpa = linha.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=linha_limpa)

# Salva o arquivo
pdf.output("Guia_CineIA.pdf")
print("PDF gerado com sucesso na pasta do seu projeto!")