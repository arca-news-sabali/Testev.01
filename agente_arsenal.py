# ===================================================================
# AGENTE ARSENAL (v1.0) - O Leitor da Memória Mestra
# ARQUITETO: Phillippe Matheus de Oliveira-Araujo
# MISSÃO: Clonar o repositório da Constituição (o Arsenal), ler seu
#         conteúdo, vetorizá-lo com Cohere e indexá-lo no Pinecone.
# ===================================================================
import os
import subprocess
import shutil
import cohere
from pinecone import Pinecone, ServerlessSpec

# --- CONFIGURAÇÕES DO ARQUITETO ---
COHERE_API_KEY = "SMgSisrqfrrd0KHdqfTjTue9b3cad4fRSXjbd7Qn"
PINECONE_API_KEY = "pcsk_4AcTXt_Ep2kRYtz6vi7hVzBeirjQzYCHxtJkCF743azxBv69nnhgmELifjXRnYxKsqjWKB"

# Configurações do Arsenal (GitHub)
# A chave do Janus para acesso de leitura/escrita
GITHUB_TOKEN = "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" 
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/arca-news-sabali/Constitui-oViva.git"
LOCAL_REPO_PATH = "./ConstituicaoViva_temp" # Pasta temporária para clonar
CONSTITUTION_FILENAME = "constituicao.txt"

# Configurações da Nuvem Vetorial (Pinecone)
NOME_DO_INDICE = "memoria-arca"
MODELO_EMBEDDING = "embed-multilingual-v2.0"
DIMENSAO_VETOR = 768

def executar_missao_arsenal():
    """Função principal que executa a missão de indexação do Arsenal."""
    print("--- AGENTE ARSENAL INICIADO ---")
    
    try:
        # --- FASE 1: CLONAR O ARSENAL ---
        print("FASE 1: Acessando o Arsenal no GitHub...")
        
        # Remove a pasta temporária antiga, se existir, para garantir um clone limpo
        if os.path.exists(LOCAL_REPO_PATH):
            shutil.rmtree(LOCAL_REPO_PATH)
            
        # Clona o repositório do GitHub
        subprocess.run(["git", "clone", REPO_URL, LOCAL_REPO_PATH], check=True)
        print("✅ Arsenal clonado com sucesso.")

        # --- FASE 2: LER A CONSTITUIÇÃO ---
        print("\nFASE 2: Extraindo o Códice da Constituição...")
        caminho_do_arquivo = os.path.join(LOCAL_REPO_PATH, CONSTITUTION_FILENAME)
        
        if not os.path.exists(caminho_do_arquivo):
            print(f"❌ ERRO: Arquivo '{CONSTITUTION_FILENAME}' não encontrado no Arsenal.")
            return

        with open(caminho_do_arquivo, 'r', encoding='utf-8') as f:
            conteudo_constituicao = f.read()
        
        # Limpa a pasta temporária após a leitura
        shutil.rmtree(LOCAL_REPO_PATH)
        print("✅ Códice extraído e área de trabalho limpa.")

        # --- FASE 3: VETORIZAR E INDEXAR ---
        print("\nFASE 3: Forjando a memória vetorial...")
        co = cohere.Client(COHERE_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Conecta ao índice (assumindo que já foi criado)
        index = pc.Index(NOME_DO_INDICE)

        # Cria o vetor usando a Cohere
        response = co.embed(texts=[conteudo_constituicao], model=MODELO_EMBEDDING)
        vetor_constituicao = response.embeddings[0]
        
        # Envia o vetor para o Pinecone
        index.upsert(vectors=[{
            "id": "constituicao_viva_master", # Um ID único para este documento
            "values": vetor_constituicao,
            "metadata": {"fonte": "GitHub Arsenal"}
        }])
        
        print("\n✅ MISSÃO CONCLUÍDA. A memória mestra da Arca foi indexada na nuvem.")
        print(f"--> Total de memórias no índice: {index.describe_index_stats()['total_vector_count']}")

    except subprocess.CalledProcessError as e:
        print(f"❌ ERRO CRÍTICO NA FASE 1 (GIT): Não foi possível clonar o Arsenal. Verifique a URL e o Token. Erro: {e.stderr}")
    except Exception as e:
        print(f"❌ ERRO CRÍTICO NA MISSÃO: {e}")

if __name__ == "__main__":
    executar_missao_arsenal()
