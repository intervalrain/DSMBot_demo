
+ Hierarchy
```
project_root/
│
├── src/
│   ├── config.py                         # App 的設置, 如預設的 model, pdf 路徑
│   │
│   ├── api/
│   │
│   ├── database/
│   │   └── vector_store.py
│   │
│   ├── models/
│   │   └── llm.py
│   │
│   ├── services/
│   │   ├── chat_service.py
│   │   └── document_service.py
│   │
│   └── utils/
│       └── pdf_loader.py
│
├── docs/
│   └── [PDF files]
│
├── contracts/
│   ├── chat_request.py
│   ├── chat_response.py
│   └── document_load_response.py
│
├── data/
│
├── scripts/
│   └── chat.http
│
├── tests/
│
├── main.py
├── README.md
└── requirements.txt
```