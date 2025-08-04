# :file_folder: RAG AI Assistant

---

## Description

RAG AI Assistant is a modular Retrieval-Augmented Generation (RAG) system designed for advanced document-based question answering, information retrieval, and cost estimation. The assistant leverages a vector database (PostgreSQL with pgvector) to store and search document embeddings, enabling efficient and context-aware responses. It supports multiple chat and embedding models, with a flexible architecture for integrating new model families. Cost estimation features help track and predict API usage expenses during document processing and Q&A.

A key component of the project is a document conversion pipeline that processes DOCX and PDF files through cleaning, conversion, enrichment, and export steps. This pipeline prepares documents for embedding and retrieval, but the main focus is on the AI assistant's ability to answer questions and interact with users based on the ingested knowledge.

## Technologies Used

- Python (3.12.3)
- PostgreSQL (with pgvector extension)
- OpenAI models (chat & embedding)
- Document processing libraries (e.g., python-docx, docx, docling, unstructured, bs4, xml.etree.ElementTree)
- Utility and system libraries (argparse, base64, json, os, re, time, pathlib)
- Concurrency and functional tools (concurrent.futures.ThreadPoolExecutor, functools.partial)
- Type hints (typing)
- OpenAI API (openai, tenacity)

## Main Classes

## Features

- RAG-based AI assistant for document Q&A
- Vector database storage and semantic search (PostgreSQL + pgvector)
- Modular model integration (multiple chat/embedding models via class methods)
- Configurable chunking and overlap for document embeddings
- Multi-step document conversion pipeline (cleaning, conversion, enrichment, export)
- Automatic summarization of images and tables using LLM models (e. g. OpenAI API)
- Cost estimation for API usage and document processing

## Installation

1. Install PostgreSQL and pgvector extension
2. Set up Python environment and install dependencies
3. Configure OpenAI API keys and database connection

```bash
# Example
pip install -r requirements.txt
# Set up PostgreSQL and pgvector
```

## Usage

1. Ingest DOCX or TXT documents using the conversion pipeline
2. Generate and store embeddings in the vector database
3. Interact with the AI assistant via chat interface for document-based Q&A
4. Extend with new chat or embedding models as needed

## Screenshots

## Project Structure

Below is a recommended repository structure for this project, following Python best practices and supporting modularity, testing, and maintainability:

```plaintext
rag-ai-assistant/
├── rag_assistant/           # Main package: core logic, models, pipelines
│   ├── __init__.py
│   ├── rag_assistant.py     # Main entry: runs QA, orchestrates RAG workflow
│   ├── document_cleaner.py  # Cleans and preprocesses documents
│   ├── chunker.py           # Splits documents into chunks for embedding
│   ├── embedding.py         # Embedding generation and management
│   ├── vector_db.py         # Vector database handler (PostgreSQL + pgvector)
│   ├── llm_api.py           # LLM API integration (e.g., OpenAI)
│   ├── cost_estimation.py   # Cost estimation for API usage and processing
│   └── ...
├── input/                   # Raw documents to be processed (DOCX, TXT)
├── output/                  # Processed files, embeddings, exported results
├── logs/                    # Log files for processing and QA runs
├── scripts/                 # CLI scripts
├── tests/                   # Unit and integration tests
│   ├── __init__.py
│   ├── test_document_cleaner.py  # Tests for document cleaning and preprocessing
│   ├── test_chunker.py           # Tests for chunking logic
│   ├── test_embedding.py         # Tests for embedding generation and management
│   ├── test_vector_db.py         # Tests for vector database operations
│   ├── test_llm_api.py           # Tests for LLM API integration
│   └── test_assistant.py         # Integration tests for RAG assistant workflow
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── LICENSE                  # License file
├── .env.example             # Example environment variables (API keys, DB config)
└── setup.py                 # (Optional) For packaging and installation
```

## License

MIT License
