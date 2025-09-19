# ===================================================================
# ARCA BACKEND v1.0 - O CÉREBRO DA ARTISTA
# ===================================================================
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# --- INICIALIZAÇÃO DA API ---
app = FastAPI()

# Configure CORS to allow all hosts (required for Replit proxy)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados para a requisição que virá do frontend
class Prompt(BaseModel):
    texto: str

# --- ROTAS DA API (PONTES DE COMUNICAÇÃO) ---

# Rota para servir a página principal da interface (index.html)
@app.get("/")
async def servir_interface():
    return FileResponse('index.html')

# Rota para servir os outros arquivos (CSS e JS)
@app.get("/{nome_arquivo}")
async def servir_arquivos(nome_arquivo: str):
    return FileResponse(nome_arquivo)

# Rota principal onde a mágica acontece: receber o prompt e retornar a resposta
@app.post("/comando_artista")
async def receber_comando(prompt: Prompt):
    print(f"Recebido comando do Arquiteto: {prompt.texto}")
    
    # --- LÓGICA DA ARTISTA (PROTÓTIPO) ---
    # Por enquanto, vamos apenas simular uma resposta.
    # No futuro, aqui é onde chamaremos o Llama3, Pinecone, etc.
    
    resposta_simulada = f"Artista recebeu seu comando: '{prompt.texto}'. Processando..."
    
    return {"resposta": resposta_simulada}

# --- EXECUÇÃO DO SERVIDOR ---
if __name__ == "__main__":
    # O uvicorn vai rodar o nosso servidor FastAPI no Replit
    uvicorn.run(app, host="0.0.0.0", port=5000)
