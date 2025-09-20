# ===================================================================
# AGENTE ARSENAL v2.0 - O INDEXADOR DA MEMÓRIA MESTRA
# ===================================================================
import os
import shutil
import cohere
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# --- FUNÇÃO PRINCIPAL DA MISSÃO ---
def executar_missao_indexacao():
    print("--- AGENTE ARSENAL INICIADO ---")

    # --- CARREGAR SEGREDOS DO COFRE LOCAL ---
    load_dotenv()
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        
    # Validação das chaves
    if not all([COHERE_API_KEY, PINECONE_API_KEY, GITHUB_TOKEN]):
        print("❌ ERRO CRÍTICO: Uma ou mais chaves de API (Cohere, Pinecone, GitHub) não foram encontradas no arquivo .env.")
        return

    # --- CONFIGURAÇÕES ---
    REPO_URL = f"https://{GITHUB_TOKEN}@github.com/arca-news-sabali/ConstituicaoViva.git"
    LOCAL_REPO_PATH = "./ConstituicaoViva_temp"
    CONSTITUTION_FILENAME = "constituicao.txt"
    PINECONE_INDEX_NAME = "memoria-arca"

    try:
        # FASE 1: ACESSAR O ARSENAL
        print("\nFASE 1: Acessando o Arsenal no GitHub...")
        if os.path.exists(LOCAL_REPO_PATH):
            shutil.rmtree(LOCAL_REPO_PATH)
            
        subprocess.run(f"git clone {REPO_URL} {LOCAL_REPO_PATH}", shell=True, check=True)
        print("✅ Arsenal clonado com sucesso.")

        # FASE 2: EXTRAIR O CÓDICE
        print("\nFASE 2: Extraindo o Códice da Constituição...")
        caminho_arquivo = os.path.join(LOCAL_REPO_PATH, CONSTITUTION_FILENAME)
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo '{CONSTITUTION_FILENAME}' não encontrado no repositório.")
            
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto_constituicao = f.read()
            
        shutil.rmtree(LOCAL_REPO_PATH)
        print("✅ Códice extraído e área de trabalho limpa.")

        # FASE 3: FORJAR A MEMÓRIA VETORIAL
        print("\nFASE 3: Forjando a memória vetorial...")
            
        # Conectar ao Cohere
        co = cohere.Client(COHERE_API_KEY)
            
        # Conectar ao Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # Verificar/Criar o índice no Pinecone
        if PINECONE_INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1024, # Dimensão para o modelo 'embed-multilingual-v3.0'
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            print(f"--> Índice '{PINECONE_INDEX_NAME}' criado no Pinecone.")

        index = pc.Index(PINECONE_INDEX_NAME)

        # Vetorizar o texto com Cohere
        response = co.embed(
            texts=[texto_constituicao],
            model='embed-multilingual-v3.0',
            input_type='search_document'
        )
        vetor = response.embeddings[0]

        # Enviar para o Pinecone
        index.upsert(vectors=[{'id': 'constituicao_viva_01', 'values': vetor, 'metadata': {'fonte': 'GitHub Arsenal'}}])
            
        stats = index.describe_index_stats()
        print("\n✅ MISSÃO CONCLUÍDA. A memória mestra da Arca foi indexada na nuvem.")
        print(f"--> Total de memórias no índice: {stats['total_vector_count']}")

    except Exception as e:
        print(f"❌ FALHA CRÍTICA NA MISSÃO DO ARSENAL: {e}")
        # Garante a limpeza mesmo em caso de erro
        if os.path.exists(LOCAL_REPO_PATH):
            shutil.rmtree(LOCAL_REPO_PATH)

if __name__ == "__main__":
    import subprocess # Adicionado para garantir que está no escopo
    executar_missao_indexacao()
