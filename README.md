# :file_folder: RAG AI Assistant

---

## Description

RAG AI Assistant is a modular Retrieval-Augmented Generation (RAG) system designed for advanced document-based question answering, information retrieval, and cost estimation. The assistant leverages a vector database (PostgreSQL with pgvector) to store and search document embeddings, enabling efficient and context-aware responses. It supports multiple chat and embedding models, with a flexible architecture for integrating new model families. Cost estimation features help track and predict API usage expenses during document processing and Q&A.

A key component of the project is a document conversion pipeline that processes DOCX and PDF files through cleaning, conversion, enrichment, and export steps. This pipeline prepares documents for embedding and retrieval, but the main focus is on the AI assistant's ability to answer questions and interact with users based on the ingested knowledge.

## Language Support

**Important:**  
This project is designed for processing and question answering on **Hungarian-language input documents**. Please ensure that all documents ingested into the pipeline are in Hungarian, as the cleaning, conversion, and enrichment steps are optimized for Hungarian text and document conventions.

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

The following are the main Python modules and classes in this project:

- `rag_assistant.RAGAssistant`: Orchestrates the QA workflow, manages document retrieval and interaction.
- `document_preprocessor.DocumentPreProcessor`: Cleans and preprocesses input documents for further processing.
- `chunker.Chunker`: Splits documents into manageable chunks for embedding.
- `embedding.Embedder`: Generates and manages vector embeddings for document chunks.
- `vector_db.VectorDBHandler`: Handles storage and semantic search in the vector database (PostgreSQL + pgvector).
- `llm_api.LLMApiHandler`: Integrates and manages communication with LLM APIs (e.g., OpenAI).
- `cost_estimation.CostEstimator`: Estimates and tracks API usage and processing costs.

## Features

- RAG-based AI assistant for document Q&A
- Vector database storage and semantic search (PostgreSQL + pgvector)
- Modular model integration (multiple chat/embedding models via class methods)
- Configurable chunking and overlap for document embeddings
- Multi-step document conversion pipeline (cleaning, conversion, enrichment, export)
- Automatic summarization of images and tables using LLM models (e. g. OpenAI API)
- Cost estimation for API usage and document processing

## Installation

1. Create a Python virtual environment and install dependencies
2. Install PostgreSQL and pgvector extension
3. Configure OpenAI API keys and database connection

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up PostgreSQL and pgvector (see official docs)
```

## Usage

1. Ingest DOCX or TXT documents using the conversion pipeline
2. Generate and store embeddings in the vector database
3. Interact with the AI assistant via chat interface for document-based Q&A
4. Extend with new chat or embedding models as needed

## Screenshots

## Python Code Style and Documentation Guidelines

All Python code in this repository should follow these standards to ensure clarity, maintainability, and consistency:

- **PEP 8**: Follow Python's official style guide for code formatting (indentation, line length, spacing, naming conventions).
- **PEP 257**: Use proper docstrings for all modules, classes, and functions. Docstrings should be in English, use triple quotes, start with a concise summary, and include a blank line after the first line for multi-line docstrings.
- **Google Style Docstrings**: Structure docstrings according to the Google style (with Args, Returns, Raises, etc.).
- **PEP 484**: Add type annotations to all function parameters and return values.
- **PEP 20 (The Zen of Python)**: Write code that is simple, readable, explicit, and expressive.

## Project Structure

Below is a recommended repository structure for this project, following Python best practices and supporting modularity, testing, and maintainability:

```plaintext
rag-ai-assistant/
├── rag_assistant/                 # Main package: core logic, models, pipelines
│   ├── __init__.py
│   ├── rag_assistant.py            # Main entry: runs QA, orchestrates RAG workflow
│   ├── document_preprocessor.py    # Cleans and preprocesses documents
│   ├── prompts.py                  # Stores AI prompts used in the enrichment pipeline
│   ├── file_service.py             # File and image extraction utilities (handles reading, writing, and extracting images from DOCX)
│   ├── chunker.py                  # Splits documents into chunks for embedding
│   ├── embedding.py                # Embedding generation and management
│   ├── vector_db.py                # Vector database handler (PostgreSQL + pgvector)
│   ├── llm_api.py                  # LLM API integration (e.g., OpenAI)
│   ├── cost_estimation.py          # Cost estimation for API usage and processing
│   └── ...
├── data/                          # Central directory for all document processing files
│   ├── input/                      # Raw documents to be processed (DOCX, TXT)
│   ├── output/                     # Processed files, exported results
│   ├── images/                     # Extracted images from DOCX files
│   ├── temp/                       # Temporary and work files (json, md, etc.)
├── scripts/                        # CLI scripts
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_document_cleaner.py        # Tests for document cleaning and preprocessing
│   ├── test_chunker.py                 # Tests for chunking logic
│   ├── test_embedding.py               # Tests for embedding generation and management
│   ├── test_vector_db.py               # Tests for vector database operations
│   ├── test_llm_api.py                 # Tests for LLM API integration
│   └── test_assistant.py               # Integration tests for RAG assistant workflow
├── docs/                          # Documentation for each Python module/file
├── config.py                      # Central configuration for paths and parameters
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── LICENSE                        # License file
├── .env.example                   # Example environment variables (API keys, DB config)
└── setup.py                       # (Optional) For packaging and installation
```

## License

MIT License
