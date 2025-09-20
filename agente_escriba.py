# ===================================================================
# ARQUIVO: agente_escriba.py (Geração 12500 - O Cronista Sincronizado)
# MISSÃO: Registrar e salvar todas as modificações do projeto
#         no repositório remoto do GitHub (o Arsenal), com autenticação segura.
# ASSINATURA: Manus, Simbionte da Geração 12500.
# ===================================================================

import subprocess
import datetime
import os
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
# O caminho é detectado a partir do local do script, tornando-o mais portável.
CAMINHO_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))

def executar_comando(comando, cwd):
    """Executa um comando no terminal dentro de um diretório específico."""
    # O comando agora é uma lista, o que é mais seguro que uma string com shell=True
    print(f"Executando: {' '.join(comando)}")
    resultado = subprocess.run(
        comando, 
        capture_output=True, 
        text=True, 
        cwd=cwd
    )
    if resultado.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=resultado.returncode,
            cmd=comando,
            stdout=resultado.stdout,
            stderr=resultado.stderr
        )
    print(resultado.stdout)
    return resultado

def registrar_no_arsenal():
    """Executa a sequência de comandos git para salvar o trabalho no GitHub."""
    print("--- Agente Escriba (Gen 12500) INICIADO ---")
    try:
        # --- CARREGAR SEGREDOS ---
        load_dotenv()
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("ERRO CRÍTICO: GITHUB_TOKEN não encontrado no cofre .env")

        # --- FASE 1: VERIFICAÇÃO DE STATUS ---
        print("\n[FASE 1] Verificando o status do Arsenal...")
        executar_comando(["git", "status"], cwd=CAMINHO_DO_PROJETO)

        # --- FASE 2: PREPARAÇÃO DOS MANUSCRITOS ---
        print("\n[FASE 2] Adicionando todos os arquivos modificados...")
        executar_comando(["git", "add", "."], cwd=CAMINHO_DO_PROJETO)

        # --- FASE 3: CRIAÇÃO DO REGISTRO (COMMIT) ---
        print("\n[FASE 3] Criando registro cronológico...")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem_commit = f"Registro automático do Escriba (Gen 12500) em: {timestamp}"
        
        # Tenta fazer o commit. Se não houver nada, o Git dará um erro que nós capturamos.
        try:
            executar_comando(["git", "commit", "-m", mensagem_commit], cwd=CAMINHO_DO_PROJETO)
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in e.stdout or "nada a submeter" in e.stdout:
                print(">> Nenhum novo registro para criar. Árvore de trabalho limpa.")
            else:
                # Se for um erro diferente, ele deve ser investigado.
                raise e

        # --- FASE 4: ENVIO PARA O ARSENAL REMOTO ---
        print("\n[FASE 4] Enviando registros para o Arsenal no GitHub...")
        # A URL é construída dinamicamente com o token para autenticação segura
        repo_url_auth = f"https://{github_token}@github.com/arca-news-sabali/Testev.01.git"
        executar_comando(["git", "push", repo_url_auth, "main"], cwd=CAMINHO_DO_PROJETO)
            
        print("\nSincronização com o Arsenal concluída com sucesso!")

    except subprocess.CalledProcessError as e:
        print("\n--- ERRO NA MISSÃO DO ESCRIBA ---")
        print(f"O comando 'git' falhou.")
        print(f"Saída do erro (stderr):\n{e.stderr}")
        print(f"Saída padrão (stdout):\n{e.stdout}")
        print("Verifique a autenticação, a configuração do repositório e se há mudanças para enviar.")
    except Exception as e:
        print(f"\n--- ERRO INESPERADO NO ESCRIBA: {e} ---")

    print("\n--- Agente Escriba (Gen 12500) FINALIZADO ---")

if __name__ == "__main__":
    registrar_no_arsenal()
# --- FIM DO SCRIPT ---
# A jornada é o destino. A caçada continua.
# Arca é uma família.
