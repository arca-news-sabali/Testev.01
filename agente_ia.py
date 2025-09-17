# ===================================================================
# ARQUIVO: exercito.py (Versão de Compatibilidade Máxima)
# ===================================================================

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Log
from textual.containers import Container
from textual.binding import Binding

try:
    from agente_arqueologo import extrair_dados_brutos
except ImportError:
    def extrair_dados_brutos():
        print("\nERRO CRÍTICO: Arquivo 'agente_arqueologo.py' não encontrado.")

class ExercitoApp(App):
    CSS_PATH = "exercito.css"
    BINDINGS = [Binding(key="q", action="quit", description="Sair do Dashboard")]

    def compose(self) -> ComposeResult:
        yield Header(name="Dashboard do Exército Manus")
        with Container(id="painel_botoes"):
            yield Button("Executar Dossiê Diário", id="btn_dossie", variant="primary")
            yield Button("Verificar Status (Em breve)", id="btn_status", variant="default", disabled=True)
        
        # Versão simplificada sem o 'border_title' para garantir que funcione
        with Static(id="container_log"):
            yield Log(id="log_missoes", auto_scroll=True)
            
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one(Log)
        if event.button.id == "btn_dossie":
            log_widget.write_line(">>> [ORDEM RECEBIDA] Iniciando missão do Agente Arqueólogo...")
            try:
                extrair_dados_brutos()
                log_widget.write_line(">>> [MISSÃO CONCLUÍDA] Agente Arqueólogo finalizou a execução.")
            except Exception as e:
                log_widget.write_line(f">>> [ERRO CRÍTICO] A missão falhou: {e}")

def main():
    app = ExercitoApp()
    app.run()

if __name__ == "__main__":
    main()
