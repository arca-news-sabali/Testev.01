# ===================================================================
# ARQUIVO: agente_arqueologo.py (v2.1 - Dossiê de Emergência)
# MISSÃO: Coletar todos os e-mails do dia, extrair a data de
#         recebimento de cada um, e enviá-los como um dossiê.
# ===================================================================

import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import date, datetime
import pytz
import re # Importa a biblioteca de expressões regulares

def extrair_dados_brutos():
    # --- CONFIGURAÇÃO ---
    EMAIL_CONTA = "arcanews.sabali@gmail.com"
    USUARIO = EMAIL_CONTA
    SENHA_DE_APP = "cwmjnwlpghdklwls"
    IMAP_SERVER = "imap.gmail.com"
    SMTP_SERVER = "smtp.gmail.com"
    EMAIL_DESTINO = "arquiteto.arca@proton.me"
    
    FUSO_HORARIO_BRASILIA = pytz.timezone('America/Sao_Paulo')
    HOJE = datetime.now(FUSO_HORARIO_BRASILIA).date()
    DATA_FORMATADA_IMAP = HOJE.strftime("%d-%b-%Y")
    DATA_FORMATADA_ASSUNTO = HOJE.strftime("%d/%m/%Y")

    print(f"--- Agente Arqueólogo v2.1 (Dossiê de Emergência) INICIADO ---")
    print(f"Fuso Horário: America/Sao_Paulo | Data da Missão: {DATA_FORMATADA_ASSUNTO}")

    # --- FASE 1: CONEXÃO E BUSCA ---
    try:
        print("\n[FASE 1] Conectando ao servidor IMAP...")
        imap = imaplib.IMAP4_SSL(IMAP_SERVER)
        imap.login(USUARIO, SENHA_DE_APP)
        imap.select("inbox")
        print("Conexão estabelecida. Buscando artefatos do dia...")
        status, mensagens = imap.search(None, f'(SENTSINCE {DATA_FORMATADA_IMAP})')
        if status != 'OK':
            print("Nenhum artefato encontrado.")
            imap.logout()
            return
        ids_emails = mensagens[0].split()
        print(f"Encontrado(s) {len(ids_emails)} artefato(s) potencial(is).")
    except Exception as e:
        print(f"ERRO na FASE 1: {e}")
        return

    # --- FASE 2: COLETA E ENRIQUECIMENTO DE DADOS ---
    artefatos_coletados = []
    corpo_dossie_texto = f"Relatório de inteligência do dia {DATA_FORMATADA_ASSUNTO}.\n\n"
    
    if ids_emails:
        print("\n[FASE 2] Coletando e enriquecendo dados...")
        for i, num in enumerate(ids_emails, 1):
            try:
                status, dados = imap.fetch(num, "(RFC822)")
                if status == 'OK':
                    conteudo_bruto_email = dados[0][1]
                    msg_obj = email.message_from_bytes(conteudo_bruto_email)
                    
                    # --- EXTRAÇÃO DE METADADOS ---
                    # Assunto
                    assunto_original, encoding = email.header.decode_header(msg_obj["Subject"])[0]
                    if isinstance(assunto_original, bytes):
                        assunto_original = assunto_original.decode(encoding or 'utf-8', 'ignore')
                    
                    # Data de Recebimento (do cabeçalho 'Received')
                    data_recebimento_str = "Data de Recebimento Indisponível"
                    received_header = msg_obj.get_all('Received', [])
                    if received_header:
                        # Pega o último cabeçalho 'Received', que é o mais próximo do destino
                        match = re.search(r';\s*(.*)', received_header[-1])
                        if match:
                            data_recebimento_str = match.group(1).strip()

                    # Adiciona os metadados ao corpo do dossiê
                    corpo_dossie_texto += f"--- Artefato {i} ---\n"
                    corpo_dossie_texto += f"Assunto: {assunto_original}\n"
                    corpo_dossie_texto += f"Recebido em: {data_recebimento_str}\n\n"

                    # Monta o nome do arquivo
                    nome_arquivo_seguro = "".join(c for c in assunto_original if c.isalnum() or c in (' ', '.', '_')).rstrip()
                    if not nome_arquivo_seguro: nome_arquivo_seguro = f"Artefato_{i}"
                    nome_artefato = f"Artefato Sagrado - {nome_arquivo_seguro[:50]}.eml"
                    
                    artefatos_coletados.append((nome_artefato, conteudo_bruto_email))
                    print(f"  - Artefato '{nome_artefato}' processado.")
            except Exception as e:
                print(f"  - Falha ao processar um artefato: {e}")
    
    imap.logout()
    print("Coleta finalizada.")

    # --- FASE 3: MONTAGEM E ENTREGA DO DOSSIÊ ---
    if not artefatos_coletados:
        print("\nNenhum artefato para entregar.")
        return

    print("\n[FASE 3] Montando e enviando o dossiê...")
    try:
        msg_dossie = MIMEMultipart()
        msg_dossie["From"] = EMAIL_CONTA
        msg_dossie["To"] = EMAIL_DESTINO
        msg_dossie["Subject"] = f"Dossiê Arqueológico de Emergência - {DATA_FORMATADA_ASSUNTO}"
        
        msg_dossie.attach(MIMEText(corpo_dossie_texto, "plain"))

        for nome_artefato, conteudo_bruto in artefatos_coletados:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(conteudo_bruto)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={nome_artefato}")
            msg_dossie.attach(part)
        
        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as smtp:
            smtp.login(USUARIO, SENHA_DE_APP)
            smtp.send_message(msg_dossie)
            print("\nDossiê de Emergência enviado com sucesso para o QG!")

    except Exception as e:
        print(f"ERRO na FASE 3: {e}")
        return

    print("\n--- Agente Arqueólogo v2.1 FINALIZADO ---")

if __name__ == "__main__":
    extrair_dados_brutos()
