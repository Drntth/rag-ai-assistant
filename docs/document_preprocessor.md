# DocumentPreProcessor Module Documentation

## Overview

`DocumentPreProcessor` is a class designed for cleaning, preprocessing, and enriching documents in the RAG AI Assistant project. It supports flexible integration with external AI providers (such as OpenAI) for advanced document enrichment, including table and image summarization. The module is highly configurable, allowing for various cleaning steps and enrichment strategies.

## Main Features

- **Document Cleaning**: Removes headers, footers, table of contents, empty paragraphs, and handles abbreviations and footnotes in DOCX files.
- **Image Extraction**: Extracts images from DOCX files and saves them to a specified directory, inserting placeholders in the document.
- **Document Conversion**: Converts DOCX and PDF files to Markdown format using Docling, and further processes Markdown to JSON using Unstructured.
- **AI Enrichment**: Enriches JSON content with table and image summaries using external AI providers (e.g., OpenAI).
- **Export**: Exports enriched JSON content to plain text files for downstream use.

## Usage Example

```python
from rag_assistant.document_preprocessor import DocumentPreProcessor

# Initialize the preprocessor
preprocessor = DocumentPreProcessor(
    data_dir="data",
    api_key="your_openai_api_key",
    api_provider="openai"
)

# Run the preprocessing pipeline on a document
preprocessor.run("input.docx")
```

## Class Reference

### DocumentPreProcessor

#### **init**(...)

Initializes the preprocessor with configuration options for cleaning and enrichment.

#### run(input_filename: str) -> None

Runs the preprocessing pipeline for the specified input file. Copies the input to a temp directory and processes it through all configured steps.

#### process_data(...)

Processes the document with the specified cleaning and enrichment steps. Handles DOCX and TXT files, supports stepwise execution.

### DOCXDocumentCleaner

Cleans and preprocesses DOCX documents. Supports header/footer removal, TOC removal, empty paragraph deletion, abbreviation extraction/modification, and footnote handling.

## Notes

- All paths should be provided as `pathlib.Path` objects or strings.
- The module is designed for extensibility and integration with external AI providers.
- Cleaning and enrichment steps are modular and can be configured via constructor arguments.
- The pipeline is robust to different document formats (DOCX, PDF, TXT).
