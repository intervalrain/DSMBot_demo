import os
from typing import List, Dict
from config import settings

class DocProvider:
    def __init__(self, doc_dir: str = settings.PDF_DIRECTORY):
        self.doc_dir = doc_dir
        self.documents = self._load_documents()
        
    def _load_documents(self) -> List[Dict]:
        documents = []
        try:
            for i, filename in enumerate(os.listdir(self.doc_dir), start=1):
                if filename.endswith(".pdf"):
                    documents.append({
                        "id": i,
                        "name": filename,
                        "path": os.path.join(self.doc_dir, filename)
                    })
        except FileNotFoundError:
            print(f"Directory {self.doc_dir} not found")
        except Exception as e:
            print(f"An error occurred: {e}")
        return documents
    
    def get_docs(self, user_id: str) -> List[Dict]:
        return self.documents

def get_doc_provider() -> DocProvider:
    return DocProvider()