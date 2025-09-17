# ===================================================================
# ARQUIVO: exercito.py
# DESCRIÇÃO: Painel de Controle principal para o Exército Manus.
# ===================================================================

# --- Importações de Bibliotecas ---
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Log
from textual.containers import Container
from textual.binding import Binding

# --- Importação do Agente ---
# Tenta importar a função principal do nosso agente.
# Se falhar, cria uma função de placeholder para não quebrar o dashboard.
try:
    from agente_arqueologo import extrair_dados_brutos
except ImportError:
    def extrair_dados_brutos():
        # Esta função será chamada se o import falhar.
        # Ela retorna uma string para ser exibida no log.
        print("\nERRO CRÍTICO: Arquivo 'agente_arqueologo.py' não encontrado.")
        print("A missão do Agente Arqueólogo não pode ser executada.")

# --- Definição da Aplicação do Dashboard ---
class ExercitoApp(App):
    """O Dashboard de Controle do Exército Manus, construído com Textual."""

    # Define o caminho para o nosso arquivo de estilo CSS.
    CSS_PATH = "exercito.css"

    # Define atalhos de teclado globais para a aplicação.
    BINDINGS = [
        Binding(key="q", action="quit", description="Sair do Dashboard"),
    ]

    def compose(self) -> ComposeResult:
        """
        Cria e organiza os widgets que compõem a interface do dashboard.
        Este método é chamado uma vez quando a aplicação inicia.
        """
        yield Header(name="Dashboard do Exército Manus")
        
        with Container(id="painel_botoes"):
            yield Button("Executar Dossiê Diário", id="btn_dossie", variant="primary")
            yield Button("Verificar Status (Em breve)", id="btn_status", variant="default", disabled=True)
        
        # Cria um contêiner com título para o nosso log de missões.
        with Static(id="container_log", border_title="Log de Missões"):
            yield Log(id="log_missoes", auto_scroll=True)
            
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
                    """Chamado quando um botão é pressionado."""
                    log_widget = self.query_one(Log)
                    
                    if event.button.id == "btn_dossie":
                        log_widget.write_line(">>> [ORDEM RECEBIDA] Iniciando missão do Agente Arqueólogo...")
                        
                        # --- TÉCNICA AVANÇADA DE CAPTURA DE SAÍDA ---
                        import io
                        import sys
                        from contextlib import redirect_stdout
                
                        # Cria um "gravador" de texto em memória
                        f = io.StringIO()
                        
                        try:
                            # Redireciona tudo que seria impresso na tela para o nosso "gravador"
                            with redirect_stdout(f):
                                extrair_dados_brutos()
                            
                            # Pega tudo o que foi "gravado"
                            log_output = f.getvalue()
                            
                            # Escreve o log capturado no nosso widget do dashboard
                            log_widget.write(log_output)
                            log_widget.write_line(">>> [MISSÃO CONCLUÍDA] Agente Arqueólogo finalizou a execução.")
                
                        except Exception as e:
                            log_widget.write_line(f">>> [ERRO CRÍTICO] A missão falhou: {e}")
                            # Se houve um erro, também imprimimos o que foi capturado até então
                            log_output = f.getvalue()
                            log_widget.write(log_output)
                

def main():
    """Função principal que inicia a aplicação do dashboard."""
    app = ExercitoApp()
    app.run()

# --- Ponto de Entrada do Script ---
# Este bloco garante que a função main() só será chamada
# quando executarmos 'python exercito.py' diretamente.
if __name__ == "__main__":
    main()
