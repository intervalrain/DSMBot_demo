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
    
    const settingItems = document.querySelectorAll('.setting-item');
    const modelOptions = document.querySelectorAll('.model-option');
    const topkSlider = document.getElementById('topk-slider');
    const topkValue = document.getElementById('topk-value');
    const temperatureSlider = document.getElementById('temperature-slider');
    const temperatureValue = document.getElementById('temperature-value');

    // default setting
    let isResizing = false;
    let currentModel = 'mistral';
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
    settingItems.forEach(item => {
        const button = item.querySelector('button');
        const options = item.querySelector('.setting-options');
    
        button.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = options.classList.contains('show');
            
            // Close all open options
            settingItems.forEach(otherItem => {
                otherItem.querySelector('.setting-options').classList.remove('show');
            });
    
            // If the clicked options weren't visible, show them
            if (!isVisible) {
                options.classList.add('show');
            }
        });
    });

    modelOptions.forEach(option => {
        option.addEventListener('click', () => {
            currentModel = option.dataset.model;
            console.log('Model changed to:', currentModel);
            modelOptions.forEach(opt => opt.classList.remove('active'));
            option.classList.add('active');
        });
    });

    topkSlider.addEventListener('input', () => {
        currentTopK = parseInt(topkSlider.value);
        topkValue.textContent = currentTopK;
        console.log('Top K changed to:', currentTopK);
    });

    temperatureSlider.addEventListener('input', () => {
        currentTemperature = parseFloat(temperatureSlider.value).toFixed(1);
        temperatureValue.textContent = currentTemperature;
        console.log('Temperature changed to:', currentTemperature);
    });

    // Close options when clicking outside
    document.addEventListener('click', () => {
        settingItems.forEach(item => {
            item.querySelector('.setting-options').classList.remove('show');
        });
    });

    // Prevent closing when clicking on the options
    document.querySelectorAll('.setting-options').forEach(options => {
        options.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
});