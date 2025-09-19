# ===================================================================
# ARQUIVO: agente_janus.py (Versão 7.0 - O Editor Cirúrgico)
# MISSÃO: Sincronizar ou Editar o Google Docs e registrar no GitHub.
# ===================================================================

import os
import json
import git
import time
import base64
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURAÇÕES ---
DOCUMENT_ID = "1i_tXK_zRQWbgeKLRVZjBJow8pu5gBi7usnK3_2Okfq4"
EMAIL_DESTINO = ["arquiteto.arca@proton.me", "arcanews.sabali@gmail.com"]
GITHUB_TOKEN = "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"
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/arca-news-sabali/Constitui-oViva.git"
LOCAL_REPO_PATH = "./ConstituicaoViva_local"
CONSTITUTION_FILENAME = "constituicao.txt"
SERVICE_ACCOUNT_FILE = 'janus.json'
DECRETO_PATH = "decreto.json"
# Escopo atualizado para permitir edição
SCOPES = ["https://www.googleapis.com/auth/documents", "https://mail.google.com/"]

# --- FUNÇÕES DO AGENTE ---

def autenticar_robo():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        print("✅ [Janus] Corpo digital autenticado.")
        return creds
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: Falha na autenticação. {e}")
        return None

def ler_documento_inteiro(service):
    """Lê o conteúdo e a estrutura de um Google Doc."""
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    content_text = ""
    # O Google Docs lê o conteúdo de trás para frente em sua estrutura, então precisamos ser cuidadosos
    # A maneira mais segura de obter o índice é pelo tamanho total do corpo do documento
    # No entanto, para encontrar texto, a leitura linear é mais simples.
    for element in document.get('body').get('content'):
        if 'paragraph' in element:
            for run in element.get('paragraph').get('elements'):
                content_text += run.get('textRun', {}).get('content', '')
    return document, content_text

def modo_editor(creds, decreto):
    """MODO EDITOR: Insere texto no Google Docs com base em um decreto."""
    print(">> [Janus] MODO EDITOR ativado. Modificando documento mestre...")
    try:
        service = build("docs", "v1", credentials=creds)
        document, content = ler_documento_inteiro(service)
        if document is None: return False, None

        texto_referencia = decreto['texto_referencia']
        novo_texto = "\n" + decreto['novo_texto']

        # Encontra a posição do final do texto de referência
        try:
            # Usamos rfind para encontrar a última ocorrência, mais seguro
            posicao_final_referencia = content.rfind(texto_referencia) + len(texto_referencia)
        except ValueError:
            print(f"❌ ERRO: Texto de referência '{texto_referencia}' não encontrado.")
            return False, None

        requests = [{'insertText': {'location': {'index': posicao_final_referencia}, 'text': novo_texto}}]
        service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()
        print("✅ [Janus] Documento mestre editado com sucesso.")
        
        # Após editar, busca o conteúdo atualizado para retornar
        _, conteudo_atualizado = ler_documento_inteiro(service)
        return True, conteudo_atualizado

    except Exception as e:
        print(f"❌ ERRO no Modo Editor: {e}")
        return False, None

def enviar_para_github(conteudo, nome_arquivo, commit_message):
    # Sua função robusta de enviar para o GitHub
    # ... (código completo da sua v6.0) ...
    # Por simplicidade, vou usar uma versão resumida aqui, mas você deve manter a sua.
    try:
        if not os.path.exists(LOCAL_REPO_PATH):
            git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
        repo = git.Repo(LOCAL_REPO_PATH)
        repo.remotes.origin.pull()
        filepath = os.path.join(LOCAL_REPO_PATH, nome_arquivo)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(conteudo)
        repo.git.add(filepath)
        repo.index.commit(commit_message)
        repo.remotes.origin.push()
        print("✅ [Janus] Cofre no GitHub atualizado com sucesso.")
        return True
    except Exception as e:
        print(f"❌ ERRO ao enviar para o GitHub: {e}")
        return False

# ... (função notificar_por_gmail da sua v6.0) ...

def main():
    print(f"--- INICIANDO AGENTE JANUS (v7.0) ---")
    creds = autenticar_robo()
    if not creds: return

    if os.path.exists(DECRETO_PATH):
        print(">> [Janus] Decreto da Artista encontrado.")
        with open(DECRETO_PATH, "r", encoding="utf-8") as f:
            decreto = json.load(f)
        os.remove(DECRETO_PATH)

        if decreto.get("acao") == "INSERIR_TEXTO":
            sucesso_edicao, conteudo_novo = modo_editor(creds, decreto)
            if sucesso_edicao and conteudo_novo:
                commit_msg = decreto.get("mensagem_commit", f"Edição via Decreto: {decreto['novo_texto'][:30]}...")
                enviar_para_github(conteudo_novo, CONSTITUTION_FILENAME, commit_msg)
                # notificar_por_gmail(creds, "Log de Edição de Decreto", f"Decreto '{commit_msg}' executado.")
        else:
            print(f"⚠️ Ação de decreto desconhecida: {decreto.get('acao')}")
    else:
        # Modo Padrão (Sincronização normal)
        print(">> [Janus] MODO PADRÃO ativado. Sincronizando...")
        service = build("docs", "v1", credentials=creds)
        _, conteudo_docs = ler_documento_inteiro(service)
        if conteudo_docs:
            enviar_para_github(conteudo_docs, CONSTITUTION_FILENAME, f"Sincronização de rotina {time.strftime('%Y-%m-%d')}")

    print("\n--- OPERAÇÃO JANUS CONCLUÍDA ---")

if __name__ == "__main__":
    main()
