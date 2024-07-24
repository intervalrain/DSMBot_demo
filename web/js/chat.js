function initChat() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function addMessage(content, isUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'user-message' : 'bot-message');
        messageElement.innerHTML = marked.parse(content);
        messageElement.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
        chatMessages.insertBefore(messageElement, chatMessages.firstChild);
        chatMessages.scrollTop = 0;
    }

    async function sendMessage() {
        const query = userInput.value.trim();
        if (query) {
            addMessage(query, true);
            userInput.value = '';
            userInput.style.height = 'auto';
            try {
                const response = await fetch('http://0.0.0.0:8000/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        query: query,
                        model: currentModel,
                        topk: currentTopK,
                        temperature: currentTemperature
                    }),
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

    // 自動調整文本區域的高度
    function autoResizeTextarea() {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight) + 'px';
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('input', autoResizeTextarea);
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}