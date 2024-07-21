document.addEventListener('DOMContentLoaded', () => {
    // chat box
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // sidebar
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const documentsList = document.getElementById('documents-list');
    const resizer = document.getElementById('resizer');

    // setting icons
    const modelSelect = document.getElementById('model-select');
    const topkSelect = document.getElementById('topk-select');
    const temperatureSelect = document.getElementById('temperature-select');
    
    // default setting
    let isResizing = false;
    let currentModel = 'gpt-3.5-turbo';
    let currentTopK = 3;
    let currentTemperature = 0.7;

    // Mock document list
    const documents = [
        { id: 1, name: "G-01 22eHV phase-0.3a version-1 design manual", content: "This is the content of Doc 1" },
        { id: 2, name: "G-02 22eHV phase-0.3a version-1 design manual", content: "This is the content of Doc 2" },
        { id: 3, name: "G-03 22eHV phase-0.3a version-1 design manual", content: "This is the content of Doc 3" },
    ];

    // Generate document list
    documents.forEach(doc => {
        const li = document.createElement('li');
        li.innerHTML = `
            <input type="checkbox" id="doc-${doc.id}" checked>
            <label for="doc-${doc.id}">${doc.name}</label>
        `;
        documentsList.appendChild(li);
    });

    // Sidebar toggle functionality
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });

    resizer.addEventListener('mousedown', (e) => {
        if (!sidebar.classList.contains('collapsed')) {
            isResizing = true;
            document.addEventListener('mousemove', resize);
            document.addEventListener('mouseup', stopResize);
        }
    });

    function resize(e) {
        if (isResizing && !sidebar.classList.contains('collapsed')) {
            const newWidth = e.clientX - sidebar.getBoundingClientRect().left;
            if (newWidth > 100 && newWidth < window.innerWidth * 0.5) {
                sidebar.style.width = newWidth + 'px';
            }
        }
    }

    function stopResize() {
        isResizing = false;
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }

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

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Settings functionality
    modelSelect.addEventListener('click', () => {
        const models = ['gpt-3.5-turbo', 'gpt-4'];
        const currentIndex = models.indexOf(currentModel);
        currentModel = models[(currentIndex + 1) % models.length];
        console.log('Model changed to:', currentModel);
        // You might want to add some visual feedback here
    });

    topkSelect.addEventListener('click', () => {
        currentTopK = prompt('Enter Top K value:', currentTopK);
        console.log('Top K changed to:', currentTopK);
    });

    temperatureSelect.addEventListener('click', () => {
        currentTemperature = prompt('Enter Temperature value (0-2):', currentTemperature);
        console.log('Temperature changed to:', currentTemperature);
    });
});