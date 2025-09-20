# ===================================================================
# ARCA BACKEND v1.0 - O CÉREBRO DA ARTISTA
# ===================================================================
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

# --- INICIALIZAÇÃO DA API ---
app = FastAPI()

# Configure CORS with secure settings for Replit environment
# Using "*" for origins but setting credentials=False to avoid CORS spec violation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Required for Replit proxy to work
    allow_credentials=False,  # Fixed: Set to False when using "*" origins
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Modelo de dados para a requisição que virá do frontend
class Prompt(BaseModel):
    texto: str

# --- ROTAS DA API (PONTES DE COMUNICAÇÃO) ---

# Health check endpoint for deployment monitoring
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ARCA Backend v1.0"}

# Rota para servir a página principal da interface (index.html)
@app.get("/")
async def servir_interface():
    return FileResponse('index.html')


# Secure routes for specific static files to maintain existing functionality
@app.get("/style.css")
async def get_css():
    if os.path.exists("style.css"):
        return FileResponse("style.css", media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS file not found")

@app.get("/script.js") 
async def get_js():
    if os.path.exists("script.js"):
        return FileResponse("script.js", media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JS file not found")

@app.get("/favicon.ico")
async def get_favicon():
    # Gracefully handle favicon requests
    raise HTTPException(status_code=404, detail="Favicon not found")

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
