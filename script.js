const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Função para adicionar mensagem na tela
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    const p = document.createElement('p');
    p.textContent = text;
    messageDiv.appendChild(p);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Rola para a última mensagem
}

// Função para enviar o comando para o backend
async function sendCommand() {
    const texto = userInput.value;
    if (texto.trim() === '') return;

    addMessage(texto, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/comando_artista', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ texto: texto }),
        });

        const data = await response.json();
        addMessage(data.resposta, 'bot');

    } catch (error) {
        console.error('Erro ao conectar com a Artista:', error);
        addMessage('Erro de conexão com o cérebro da Artista.', 'bot');
    }
}

// Event Listeners
sendButton.addEventListener('click', sendCommand);
userInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendCommand();
    }
});
