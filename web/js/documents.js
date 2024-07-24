function initDocuments() {
    const documentsList = document.getElementById('documents-list');

    async function getDocuments() {
        try {
            const response = await fetch('http://0.0.0.0:8000/auth_documents');
            if (!response.ok) {
                throw new Error(`Failed to fetch documents: ${response.status}`);
            }
            const data = await response.json();
            return data.documents;
        } catch (error) {
            console.error('Error:', error);
            return [];
        }
    }

    async function generateDocumentList() {
        const documents = await getDocuments();
        documents.forEach(doc => {
            const li = document.createElement('li');
            li.innerHTML = `
                <input type="checkbox" id="doc-${doc.id}" checked>
                <label for="doc-${doc.id}">${doc.name}</label>
            `;
            documentsList.appendChild(li);
        });
    }

    generateDocumentList();
}