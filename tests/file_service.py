import base64
import json

from rag_assistant.file_service import FileService


def test_write_and_read_text(tmp_path):
    file = tmp_path / "test.txt"
    FileService.write_text("hello world", file)
    assert file.read_text() == "hello world"
    assert FileService.read_text(file) == "hello world"
    assert FileService.read_lines(file) == ["hello world"]


def test_write_and_read_json(tmp_path):
    file = tmp_path / "test.json"
    data = [{"a": 1, "b": 2}]
    FileService.write_json(data, file)
    assert json.loads(file.read_text()) == data
    assert FileService.read_json(file) == data


def test_write_and_read_binary(tmp_path):
    file = tmp_path / "test.bin"
    data = b"abc123"
    FileService.write_binary(data, file)
    assert file.read_bytes() == data


def test_encode_image_base64(tmp_path):
    file = tmp_path / "testimg.png"
    file.write_bytes(b"\x89PNG\r\n\x1a\n")
    encoded = FileService.encode_image_base64(file)
    assert base64.b64decode(encoded) == b"\x89PNG\r\n\x1a\n"


def test_extract_images_from_docx(tmp_path):
    from docx import Document

    docx_path = tmp_path / "test.docx"
    doc = Document()
    doc.add_paragraph("No images here")
    doc.save(docx_path)
    images_dir = tmp_path / "images"
    FileService.extract_images_from_docx(docx_path, images_dir)
    assert images_dir.exists()
    assert len(list(images_dir.iterdir())) == 0
