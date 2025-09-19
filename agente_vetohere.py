# ===================================================================
# AGENTE INDEXADOR (v6.0 - Versão Final e Corrigida)
# ===================================================================
import os
import cohere
from pinecone import Pinecone, ServerlessSpec

# --- CONFIGURAÇÕES ---
COHERE_API_KEY = "SMgSisrqfrrd0KHdqfTjTue9b3cad4fRSXjbd7Qn"
PINECONE_API_KEY = "pcsk_4AcTXt_Ep2kRYtz6vi7hVzBeirjQzYCHxtJkCF743azxBv69nnhgmELifjXRnYxKsqjWKB"
    
NOME_DO_INDICE = "memoria-arca"
MODELO_EMBEDDING = "embed-multilingual-v2.0"
DIMENSAO_VETOR = 768

PASTA_FONTES = os.path.expanduser('~')

def executar_missao_indexacao():
    print("--- AGENTE INDEXADOR (v6.0) INICIADO ---")
    try:
        print("FASE 1: Conectando aos sistemas neurais...")
        co = cohere.Client(COHERE_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)
            
        if NOME_DO_INDICE not in pc.list_indexes().names():
            print(f"--> Índice '{NOME_DO_INDICE}' não encontrado. Criando...")
            pc.create_index(
                name=NOME_DO_INDICE,
                dimension=DIMENSAO_VETOR, 
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            print("--> Índice criado com sucesso na nuvem.")
            
        index = pc.Index(NOME_DO_INDICE)
        print("✅ Conexões estabelecidas.")

        print("\nFASE 2: Lendo artefatos de texto...")
        textos_para_ler = []
        nomes_dos_arquivos = []
        for filename in os.listdir(PASTA_FONTES):
            if filename.startswith("paradoxo") and filename.endswith(".txt"):
                filepath = os.path.join(PASTA_FONTES, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    textos_para_ler.append(f.read())
                    nomes_dos_arquivos.append(filename)
                print(f"--> Artefato '{filename}' lido.")

        if not textos_para_ler:
            print("⚠️ Nenhum artefato encontrado. Missão abortada.")
            return

        print("\nFASE 3: Criando memórias vetoriais com Cohere...")
        response = co.embed(texts=textos_para_ler, model=MODELO_EMBEDDING)
        vetores = response.embeddings
            
        print("--> Enviando memórias para a nuvem Pinecone...")
        dados_para_pinecone = []
        for i, vetor in enumerate(vetores):
            dados_para_pinecone.append({
                "id": nomes_dos_arquivos[i],
                "values": vetor,
                "metadata": {"texto": textos_para_ler[i]}
            })

        index.upsert(vectors=dados_para_pinecone)
            
        print("\n✅ MISSÃO CONCLUÍDA.")
        print(f"--> Total de memórias na nuvem: {index.describe_index_stats()['total_vector_count']}")
            
    except Exception as e:
        print(f"❌ ERRO CRÍTICO NA MISSÃO: {e}")

if __name__ == "__main__":
    executar_missao_indexacao()
