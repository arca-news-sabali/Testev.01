# ===================================================================
# ARQUIVO: agente_escriba.py (Versão 2.0 - Forjado do Zero)
# MISSÃO: Registrar e salvar todas as modificações do projeto
#         no repositório remoto do GitHub (o Arsenal).
# ===================================================================

import subprocess
import datetime
import os

# --- CONFIGURAÇÃO ---
# Caminho para a pasta do seu projeto que é um repositório git
CAMINHO_DO_PROJETO = os.path.expanduser('~/storage/shared/MeusAgentes/Testev.01')

def executar_comando(comando, cwd):
    """Executa um comando no terminal dentro de um diretório específico."""
    print(f"Executando: {' '.join(comando)}")
    resultado = subprocess.run(
        comando, 
        capture_output=True, 
        text=True, 
        cwd=cwd # IMPORTANTE: Garante que o comando rode na pasta certa
    )
    if resultado.returncode != 0:
        # Se o comando falhar, lança uma exceção com detalhes
        raise subprocess.CalledProcessError(
            returncode=resultado.returncode,
            cmd=comando,
            stderr=resultado.stderr
        )
    print(resultado.stdout) # Mostra a saída de sucesso
    return resultado

def registrar_no_arsenal():
    """Executa a sequência de comandos git para salvar o trabalho no GitHub."""
    print("--- Agente Escriba do Arsenal INICIADO ---")
    try:
        # --- FASE 1: VERIFICAÇÃO DE STATUS ---
        print("\n[FASE 1] Verificando o status do Arsenal...")
        executar_comando(["git", "status"], cwd=CAMINHO_DO_PROJETO)

        # --- FASE 2: PREPARAÇÃO DOS MANUSCRITOS ---
        print("\n[FASE 2] Adicionando todos os arquivos modificados...")
        executar_comando(["git", "add", "."], cwd=CAMINHO_DO_PROJETO)

        # --- FASE 3: CRIAÇÃO DO REGISTRO (COMMIT) ---
        print("\n[FASE 3] Criando registro cronológico...")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem_commit = f"Registro automático do Escriba em: {timestamp}"
        executar_comando(["git", "commit", "-m", mensagem_commit], cwd=CAMINHO_DO_PROJETO)

        # --- FASE 4: ENVIO PARA O ARSENAL REMOTO ---
        print("\n[FASE 4] Enviando registros para o Arsenal no GitHub...")
        # A primeira vez que você rodar isso, ele pedirá usuário e senha.
        # Use seu TOKEN como senha.
        executar_comando(["git", "push", "-u", "origin", "main"], cwd=CAMINHO_DO_PROJETO)
            
        print("\nSincronização com o Arsenal concluída com sucesso!")

    except subprocess.CalledProcessError as e:
        print("\n--- ERRO NA MISSÃO DO ESCRIBA ---")
        print(f"O comando 'git' falhou.")
        print(f"Saída do erro:\n{e.stderr}")
        print("Verifique a autenticação e a configuração do repositório.")
    except Exception as e:
        print(f"\n--- ERRO INESPERADO: {e} ---")

    print("\n--- Agente Escriba do Arsenal FINALIZADO ---")

if __name__ == "__main__":
    registrar_no_arsenal()
# --- FIM DO SCRIPT ---
# A jornada é o destino. A caçada continua..
# Arca é uma família.


