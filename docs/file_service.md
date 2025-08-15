# FileService Module Documentation

## Overview

`FileService` is a utility class providing static methods for file operations in the RAG AI Assistant project. It supports reading, writing, and processing files, including extracting images from DOCX documents and encoding images to base64. This module centralizes file management tasks to ensure clean, maintainable, and reusable code.

## Main Features

- **Image Extraction from DOCX**: Extracts images from DOCX files and saves them to a specified directory, inserting placeholders in the document.
- **Read/Write JSON**: Reads and writes JSON data to and from files.
- **Read/Write Text**: Reads and writes plain text files.
- **Read Binary**: Writes binary data to files.
- **Read Lines**: Reads lines from text files as a list.
- **Encode Image to Base64**: Encodes image files to base64 strings for API or web use.

## Usage Example

```python
from pathlib import Path
from rag_assistant.file_service import FileService

# Extract images from a DOCX file
FileService.extract_images_from_docx(Path('input.docx'), Path('images/'))

# Write JSON data
FileService.write_json([{"key": "value"}], Path('output.json'))

# Read text from a file
text = FileService.read_text(Path('input.txt'))

# Encode image to base64
b64 = FileService.encode_image_base64(Path('images/image_1.png'))
```

## Method Reference

### extract_images_from_docx(source_file: Path, images_dir: Path) -> None

Extracts images from a DOCX file and saves them to `images_dir`. Inserts placeholders in the document for each image.

### write_json(data: List[Dict], output_path: Path) -> None

Writes JSON data to a file. Raises `RuntimeError` if writing fails.

### write_binary(data: bytes, output_path: Path) -> None

Writes binary data to a file.

### write_text(text: str, output_path: Path) -> None

Writes text to a file.

### read_text(input_path: Path) -> str

Reads and returns text from a file.

### read_lines(input_path: Path) -> List[str]

Reads and returns lines from a file as a list of strings.

### read_json(input_path: Path) -> List[Dict]

Reads and returns JSON data from a file.

### encode_image_base64(image_path: Path) -> str

Encodes an image file to a base64 string.

## Notes

- All methods are static and can be called without instantiating `FileService`.
- Paths should be provided as `pathlib.Path` objects for consistency.
- The module is designed to be reusable across the project for any file management needs.
