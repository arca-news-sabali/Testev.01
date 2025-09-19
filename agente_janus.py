# agente_janus.py - Versão 6.0 (O Executor de Decretos)
# Modelo padrão para agentes executores do Ecossistema Arca.
# Este agente possui dois modos de operação:
# 1. MODO PADRÃO: Sincroniza um Google Doc pré-definido com o GitHub.
# 2. MODO DECRETO: Executa uma ordem específica emitida pela Artista,
#    encontrada em um arquivo 'decreto.json'.

import os
import git
import base64
import time
import json
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURAÇÕES DO ARQUITETO ---
# Configurações para o MODO PADRÃO
DEFAULT_DOCUMENT_ID = "1i_tXK_zRQWbgeKLRVZjBJow8pu5gBi7usnK3_2Okfq4" # ID do Doc a ser sincronizado por padrão
DEFAULT_FILENAME = "constituicao.txt"

# Configurações Gerais
EMAIL_DESTINO = ["arquiteto.arca@proton.me", "arcanews.sabali@gmail.com"] # Lista de e-mails para notificação
GITHUB_TOKEN = "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" # Seu token do GitHub
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/arca-news-sabali/Constitui-oViva.git"
LOCAL_REPO_PATH = "./ConstituicaoViva_local"
SERVICE_ACCOUNT_FILE = 'janus.json'
SCOPES = [ # Escopos de Superusuário
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://mail.google.com/",
    "https://www.googleapis.com/auth/calendar"
]

# --- FUNÇÕES DO AGENTE ---

def autenticar_robo():
    """Autentica usando a chave da Conta de Serviço."""
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        print("✅ [Janus] Corpo digital autenticado com sucesso.")
        return creds
    except FileNotFoundError:
        print(f"❌ ERRO CRÍTICO: A alma do robô ('{SERVICE_ACCOUNT_FILE}') não foi encontrada.")
        return None
    except Exception as e:
        print(f"❌ ERRO na autenticação do robô: {e}")
        return None

def buscar_do_google_docs(creds, document_id):
    """Busca o conteúdo de um Google Doc específico."""
    print(f">> [Janus] Acessando Google Docs para ler o documento ID: ...{document_id[-10:]}")
    try:
        service = build("docs", "v1", credentials=creds)
        document = service.documents().get(documentId=document_id).execute()
        content = ""
        for element in document.get("body").get("content"):
            if "paragraph" in element:
                for run in element.get("paragraph").get("elements"):
                    content += run.get("textRun", {}).get("content", "")
        print("✅ [Janus] Documento lido com sucesso.")
        return content
    except HttpError as err:
        print(f"❌ ERRO ao buscar do Google Docs: {err}")
        return None

def enviar_para_github(conteudo, nome_arquivo, commit_message):
    """Envia o conteúdo para um arquivo específico no repositório do GitHub."""
    print(">> [Janus] Verificando o cofre no GitHub...")
    try:
        os.system(f'git config --global user.name "Agente Janus"')
        os.system(f'git config --global user.email "janus.bot@arcanet.io"')

        if not os.path.exists(LOCAL_REPO_PATH):
            print(">> [Janus] Cofre local não encontrado. Clonando do GitHub...")
            git.Repo.clone_from(REPO_URL, LOCAL_REPO_PATH)
        
        repo = git.Repo(LOCAL_REPO_PATH)
        print(">> [Janus] Sincronizando com o cofre remoto...")
        repo.remotes.origin.pull()

        filepath = os.path.join(LOCAL_REPO_PATH, nome_arquivo)
        
        mudanca_detectada = True
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f_read:
                if f_read.read() == conteudo:
                    print(f">> [Janus] Nenhuma mudança detectada para o arquivo '{nome_arquivo}'. O cofre já está sincronizado.")
                    mudanca_detectada = False
        
        if mudanca_detectada:
            print(f">> [Janus] Mudança detectada. Atualizando o arquivo '{nome_arquivo}'...")
            with open(filepath, "w", encoding="utf-8") as f_write:
                f_write.write(conteudo)
            
            repo.git.add(filepath)
            repo.index.commit(commit_message)
            repo.remotes.origin.push()
            print("✅ [Janus] Cofre no GitHub atualizado com sucesso.")
        
        return mudanca_detectada
    except Exception as e:
        print(f"❌ ERRO ao enviar para o GitHub: {e}")
        return False

def notificar_por_gmail(creds, assunto, corpo):
    """Envia uma notificação por e-mail para a lista de destinos."""
    print(">> [Janus] Preparando notificação para o Arquiteto...")
    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEText(corpo, 'plain', 'utf-8')
        message["to"] = ", ".join(EMAIL_DESTINO) # Envia para todos os e-mails da lista
        message["from"] = "me"
        message["subject"] = assunto
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"✅ [Janus] Notificação '{assunto}' enviada.")
    except HttpError as err:
        print(f"❌ ERRO ao enviar e-mail: {err}")

def main():
    """Função principal que define o modo de operação do agente."""
    print("--- INICIANDO AGENTE JANUS (v6.0) ---")
    
    # MODO DECRETO: Verifica se há uma ordem da Artista
    if os.path.exists("decreto.json"):
        print(">> [Janus] MODO DECRETO ativado. Lendo ordem da Artista...")
        with open("decreto.json", "r", encoding="utf-8") as f:
            decreto = json.load(f)
        
        conteudo = decreto.get("novo_texto", "")
        nome_arquivo = decreto.get("nome_arquivo")
        commit_msg = decreto.get("mensagem_commit")

        if not nome_arquivo:
            print("❌ ERRO no decreto: 'nome_arquivo' não especificado.")
            return

        creds = autenticar_robo()
        if not creds: return

        houve_mudanca = enviar_para_github(conteudo, nome_arquivo, commit_msg)
        
        if houve_mudanca:
            corpo_email = f"Uma mudança foi decretada pela Artista e executada com sucesso.\n\nMensagem: {commit_msg}\n\nO arquivo '{nome_arquivo}' foi atualizado."
            notificar_por_gmail(creds, "Log de Execução de Decreto da Arca", corpo_email)
        
        os.remove("decreto.json")
        print(">> [Janus] Decreto executado e arquivado.")

    # MODO PADRÃO: Se não houver decreto, executa a sincronização normal
    else:
        print(">> [Janus] MODO PADRÃO ativado. Sincronizando Google Docs...")
        creds = autenticar_robo()
        if not creds: return

        conteudo_docs = buscar_do_google_docs(creds, DEFAULT_DOCUMENT_ID)
        if conteudo_docs is None: return

        commit_msg = f"Sincronização automática de '{DEFAULT_FILENAME}' em {time.strftime('%Y-%m-%d %H:%M:%S')}"
        houve_mudanca = enviar_para_github(conteudo_docs, DEFAULT_FILENAME, commit_msg)
        
        if houve_mudanca:
            corpo_email = f"O documento '{DEFAULT_FILENAME}' foi atualizado com sucesso no cofre do GitHub."
            notificar_por_gmail(creds, "Log de Sincronização da Constituição da Arca", corpo_email)
    
    print("\n--- OPERAÇÃO JANUS CONCLUÍDA ---")

if __name__ == "__main__":
    main()
