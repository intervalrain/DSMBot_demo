document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(content, isUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.textContent = content;
        chatMessages.insertBefore(messageElement, chatMessages.firstChild);
        chatMessages.scrollTop = 0;
    }

    async function sendMessage() {
        const query = userInput.value.trim();
        if (query) {
            addMessage(query, true);
            userInput.value = '';

            try {
                const response = await fetch('http://0.0.0.0:8000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query }),
                });

                if (response.ok) {
                    const data = await response.json();
                    addMessage(data.response, false);
                } else {
                    addMessage('Error: Unable to get response from the server.', false);
                }
            } catch (error) {
                console.error('Error:', error);
                addMessage('Error: Unable to connect to the server.', false);
            }
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});