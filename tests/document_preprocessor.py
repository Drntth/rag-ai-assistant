"""
Unit tests for document preprocessing components.

This module contains tests for the document preprocessor pipeline, including cleaning,
conversion, enrichment, and export functionalities.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from rag_assistant.document_preprocessor import (
    DoclingConverter,
    DocumentPreProcessor,
    DOCXDocumentCleaner,
    Enrichment,
    Export,
    UnstructuredConverter,
)


class TestDocumentPreProcessor:
    """
    Tests for the DocumentPreProcessor class.
    """

    def setup_method(self) -> None:
        """
        Set up a DocumentPreProcessor instance for testing.
        """
        self.data_dir: str = "/tmp/data"
        self.preproc: DocumentPreProcessor = DocumentPreProcessor(
            data_dir=self.data_dir,
            steps=6,
            remove_headers=True,
            remove_footers=True,
            remove_toc=True,
            remove_empty=True,
            abbreviation_strategy="inline",
            footnote_handling="remove",
            process_table_with_ai=True,
            process_images_with_ai=True,
            api_key="testkey",
            api_provider="openai",
        )
        self.preproc.text_model = "gpt-4o-mini"
        self.preproc.image_model = "gpt-4o-mini"

    def test_init_sets_attributes(self) -> None:
        """
        Test that initialization sets all attributes correctly.
        """
        assert self.preproc.data_dir == self.data_dir
        assert self.preproc.input_dir.endswith("input")
        assert self.preproc.output_dir.endswith("output")
        assert self.preproc.images_dir.endswith("images")
        assert self.preproc.temp_dir.endswith("temp")
        assert self.preproc.steps == 6
        assert self.preproc.remove_headers is True
        assert self.preproc.remove_footers is True
        assert self.preproc.remove_toc is True
        assert self.preproc.remove_empty is True
        assert self.preproc.abbreviation_strategy == "inline"
        assert self.preproc.footnote_handling == "remove"
        assert self.preproc.process_table_with_ai is True
        assert self.preproc.process_images_with_ai is True
        assert self.preproc.api_key == "testkey"
        assert self.preproc.api_provider == "openai"

    @patch("rag_assistant.document_preprocessor.shutil.copy2")
    @patch("rag_assistant.document_preprocessor.OpenAI")
    @patch.object(DocumentPreProcessor, "process_data")
    def test_run_calls_process_data_and_copies(
        self,
        mock_process_data: MagicMock,
        mock_openai: MagicMock,
        mock_copy2: MagicMock,
    ) -> None:
        """
        Test that run() calls process_data and copies the file.

        Args:
            mock_process_data: Mock for process_data method.
            mock_openai: Mock for OpenAI client.
            mock_copy2: Mock for shutil.copy2.
        """
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        self.preproc.run("test.docx")
        mock_copy2.assert_called_once()
        mock_process_data.assert_called_once()
        assert self.preproc.text_model == "gpt-4o-mini"
        assert self.preproc.image_model == "gpt-4o-mini"

    @patch("rag_assistant.file_service.FileService.extract_images_from_docx")
    @patch("rag_assistant.document_preprocessor.DOCXDocumentCleaner")
    @patch("rag_assistant.document_preprocessor.DoclingConverter")
    @patch("rag_assistant.document_preprocessor.UnstructuredConverter")
    @patch("rag_assistant.document_preprocessor.Enrichment")
    @patch("rag_assistant.document_preprocessor.Export")
    def test_process_data_docx_full_pipeline(
        self,
        mock_export: MagicMock,
        mock_enrichment: MagicMock,
        mock_unstructured: MagicMock,
        mock_docling: MagicMock,
        mock_cleaner: MagicMock,
        mock_extract_images: MagicMock,
    ) -> None:
        """
        Test the full pipeline for DOCX processing.

        Args:
            mock_export: Mock for Export class.
            mock_enrichment: Mock for Enrichment class.
            mock_unstructured: Mock for UnstructuredConverter class.
            mock_docling: Mock for DoclingConverter class.
            mock_cleaner: Mock for DOCXDocumentCleaner class.
            mock_extract_images: Mock for FileService.extract_images_from_docx.
        """
        mock_cleaner_instance = MagicMock()
        mock_cleaner.return_value = mock_cleaner_instance
        mock_cleaner_instance.abbreviation_extractors.return_value = {
            "MNB": ["Magyar Nemzeti Bank"]
        }
        mock_docling_instance = MagicMock()
        mock_docling.return_value = mock_docling_instance
        mock_unstructured_instance = MagicMock()
        mock_unstructured.return_value = mock_unstructured_instance
        mock_enrichment_instance = MagicMock()
        mock_enrichment.return_value = mock_enrichment_instance
        mock_export_instance = MagicMock()
        mock_export.return_value = mock_export_instance

        input_path: str = "/tmp/data/input/test.docx"
        output_path: str = "/tmp/data/output/test.docx"
        self.preproc.process_data(
            client=None,
            input_path=input_path,
            output_path=output_path,
            steps=6,
            remove_headers=True,
            remove_footers=True,
            remove_toc=True,
            remove_empty=True,
            abbreviation_strategy="inline",
            footnote_handling="remove",
            process_table_with_ai=True,
            process_images_with_ai=True,
        )
        # Step 1: cleaning
        mock_extract_images.assert_called()
        mock_cleaner.assert_called()
        mock_cleaner_instance.remove_headers.assert_called()
        mock_cleaner_instance.remove_footers.assert_called()
        mock_cleaner_instance.remove_toc.assert_called()
        mock_cleaner_instance.remove_empty.assert_called()
        mock_cleaner_instance.abbreviation_extractors.assert_called()
        mock_cleaner_instance.abbreviation_modifiers.assert_called()
        mock_cleaner_instance.footnote_handling.assert_called()
        # Step 2: docling
        mock_docling.assert_called()
        mock_docling_instance.validate_document.assert_called()
        mock_docling_instance.docling_process_document.assert_called()
        mock_docling_instance.clean_markdown_file.assert_called()
        mock_docling_instance.replace_image_placeholders_with_markdown.assert_called()
        # Step 3: unstructured
        mock_unstructured.assert_called()
        mock_unstructured_instance.unstructured_process_markdown.assert_called()
        # Step 4: enrichment
        mock_enrichment.assert_called()
        mock_enrichment_instance.enrich_json.assert_called()
        # Step 5: export
        mock_export.assert_called()
        mock_export_instance.export_text_from_enriched_json.assert_called()


class TestDOCXDocumentCleaner:
    def setup_method(self) -> None:
        """Set up the DOCXDocumentCleaner instance and mocks for testing.

        This method initializes the required mocks and the cleaner instance.
        """
        patcher = patch("rag_assistant.document_preprocessor.Document")
        self.mock_document = patcher.start()
        self.addCleanup = patcher.stop
        self.source_file: Path = Path("/tmp/source.docx")
        self.mock_doc: MagicMock = MagicMock()
        self.mock_document.return_value = self.mock_doc
        self.cleaner: DOCXDocumentCleaner = DOCXDocumentCleaner(self.source_file)
        self.cleaner.doc = self.mock_doc

    def teardown_method(self) -> None:
        """Clean up after each test method."""
        self.addCleanup()

    def test_init_sets_attributes(self) -> None:
        """Test that initialization sets all attributes correctly."""
        assert self.cleaner.source_file == self.source_file
        self.mock_document.assert_called_with(str(self.source_file))

    def test_remove_headers(self) -> None:
        """Test that remove_headers clears header paragraphs and saves the document."""
        mock_section: MagicMock = MagicMock()
        mock_header: MagicMock = MagicMock()
        mock_paragraph: MagicMock = MagicMock()
        mock_header.paragraphs = [mock_paragraph]
        mock_section.header = mock_header
        self.mock_doc.sections = [mock_section]
        self.cleaner.remove_headers()
        mock_paragraph.clear.assert_called_once()
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_remove_footers(self) -> None:
        """Test that remove_footers clears footer paragraphs and saves the document."""
        mock_section: MagicMock = MagicMock()
        mock_footer: MagicMock = MagicMock()
        mock_paragraph: MagicMock = MagicMock()
        mock_footer.paragraphs = [mock_paragraph]
        mock_section.footer = mock_footer
        self.mock_doc.sections = [mock_section]
        self.cleaner.remove_footers()
        mock_paragraph.clear.assert_called_once()
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_remove_toc_runs_all_methods_and_saves(self) -> None:
        """Test that remove_toc runs all TOC removal methods and saves the document."""
        toc_methods = [
            "remove_toc_by_xml",
            "remove_toc_by_field",
            "remove_toc_by_paragraphs",
            "remove_toc_by_text",
            "remove_toc_by_table",
            "remove_toc_original",
        ]
        for method_name in toc_methods:
            setattr(self.cleaner, method_name, MagicMock(return_value=False))
        self.mock_doc.save = MagicMock()
        self.cleaner.remove_toc()
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_remove_empty(self) -> None:
        """Test that remove_empty removes empty paragraphs and saves the document."""
        mock_para1: MagicMock = MagicMock()
        mock_para2: MagicMock = MagicMock()
        mock_para3: MagicMock = MagicMock()
        mock_para1.text.strip.return_value = ""
        mock_para1.runs = []
        mock_para1._element.xpath.return_value = []
        mock_para1._element.getparent.return_value.tag = "w:body"
        mock_para2.text.strip.return_value = "not empty"
        mock_para2.runs = []
        mock_para2._element.xpath.return_value = []
        mock_para2._element.getparent.return_value.tag = "w:body"
        mock_para3.text.strip.return_value = ""
        mock_para3.runs = []
        mock_para3._element.xpath.side_effect = (
            lambda x: [1] if x == ".//w:sectPr" else []
        )
        mock_para3._element.getparent.return_value.tag = "w:sectPr"
        self.mock_doc.paragraphs = [mock_para1, mock_para2, mock_para3]
        self.cleaner.remove_empty()
        mock_para1._element.getparent.return_value.remove.assert_called_once_with(
            mock_para1._element
        )
        assert not mock_para3._element.getparent.return_value.remove.called
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    @patch("rag_assistant.file_service.FileService.write_json")
    def test_abbreviation_extractors(self, mock_write_json: MagicMock) -> None:
        """Test that abbreviation_extractors finds abbreviations and writes JSON.

        Args:
            mock_write_json: Mock for FileService.write_json.
        """
        mock_para1: MagicMock = MagicMock()
        mock_para2: MagicMock = MagicMock()
        mock_para1.text = "Magyar Nemzeti Bank (a továbbiakban: MNB)"
        mock_para2.text = "Ez egy sima szöveg."
        self.mock_doc.paragraphs = [mock_para1, mock_para2]
        output_path: str = "/tmp/abbr.json"
        result = self.cleaner.abbreviation_extractors(output_path)
        assert "MNB" in result
        assert any("Magyar Nemzeti Bank" in d for d in result["MNB"])
        mock_write_json.assert_called_once_with(result, output_path)

    def test_abbreviation_modifiers_remove_phrase(self) -> None:
        """Test that abbreviation_modifiers removes phrase and saves the document."""
        mock_para: MagicMock = MagicMock()
        mock_para.text = "Magyar Nemzeti Bank (a továbbiakban: MNB)"
        self.mock_doc.paragraphs = [mock_para]
        abbreviations: dict[str, list[str]] = {"MNB": ["Magyar Nemzeti Bank"]}
        self.cleaner.abbreviation_modifiers(abbreviations, strategy="none")
        assert mock_para.text == "Magyar Nemzeti Bank (MNB)"
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_abbreviation_modifiers_inline(self) -> None:
        """Test that abbreviation_modifiers adds inline abbreviation and saves the document."""
        mock_para: MagicMock = MagicMock()
        mock_para.text = "Az MNB fontos szerepet tölt be."
        self.mock_doc.paragraphs = [mock_para]
        abbreviations: dict[str, list[str]] = {"MNB": ["Magyar Nemzeti Bank"]}
        self.cleaner.abbreviation_modifiers(abbreviations, strategy="inline")
        assert "MNB (Magyar Nemzeti Bank)" in mock_para.text
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_abbreviation_modifiers_section(self) -> None:
        """Test that abbreviation_modifiers adds section for abbreviations and saves the document."""
        mock_para: MagicMock = MagicMock()
        mock_para.text = "Első bekezdés."
        mock_insert: MagicMock = MagicMock()
        mock_para.insert_paragraph_before.return_value = mock_insert
        self.mock_doc.paragraphs = [mock_para]
        self.mock_doc.styles = {"Normal": MagicMock()}
        abbreviations: dict[str, list[str]] = {"MNB": ["Magyar Nemzeti Bank"]}
        self.cleaner.abbreviation_modifiers(abbreviations, strategy="section")
        assert mock_para.insert_paragraph_before.call_count >= 3
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_footnote_handling_remove(self) -> None:
        """Test that footnote_handling removes footnotes and saves the document."""
        mock_para: MagicMock = MagicMock()
        mock_para._element.xpath.return_value = [MagicMock()]
        mock_el: MagicMock = mock_para._element.xpath.return_value[0]
        mock_parent: MagicMock = MagicMock()
        mock_el.getparent.return_value = mock_parent
        mock_para.text = "Ez egy szöveg [*] ^1"
        self.mock_doc.paragraphs = [mock_para]
        self.cleaner.footnote_handling("remove")
        mock_parent.remove.assert_called_once_with(mock_el)
        assert "[*]" not in mock_para.text and "^1" not in mock_para.text
        self.mock_doc.save.assert_called_once_with(str(self.source_file))

    def test_footnote_handling_insert(self) -> None:
        """Test that footnote_handling inserts footnote content and saves the document."""
        mock_run: MagicMock = MagicMock()
        mock_run.text = "Run text"
        mock_run._element.xpath.return_value = [MagicMock()]
        mock_ref: MagicMock = mock_run._element.xpath.return_value[0]
        mock_ref.attrib = {"{ns}id": "1"}
        mock_ref.getparent.return_value = MagicMock()
        mock_para: MagicMock = MagicMock()
        mock_para.runs = [mock_run]
        self.mock_doc.paragraphs = [mock_para]
        mock_rel: MagicMock = MagicMock()
        mock_rel.reltype = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes"
        mock_footnote_part: MagicMock = MagicMock()
        mock_footnote_part.blob = b'<w:footnotes xmlns:w="ns"><w:footnote w:id="1"><w:t>Footnote content</w:t></w:footnote></w:footnotes>'
        mock_rel._target = mock_footnote_part
        self.mock_doc.part.rels.values.return_value = [mock_rel]

        orig_fromstring = ET.fromstring

        def fake_fromstring(blob: bytes) -> object:
            return orig_fromstring(blob)

        ET.fromstring = fake_fromstring
        self.cleaner.footnote_handling("insert")
        assert "<<lábjegyzet: Footnote content>>" in mock_run.text
        self.mock_doc.save.assert_called_once_with(str(self.source_file))
        ET.fromstring = orig_fromstring


class TestDoclingConverter:
    def setup_method(self) -> None:
        """Set up the DoclingConverter instance for testing.

        Initializes the source, markdown, and images paths and the converter instance.
        """
        self.source_file: Path = Path("/tmp/source.docx")
        self.markdown_file: Path = Path("/tmp/test.md")
        self.images_dir: str = "images"
        self.converter: DoclingConverter = DoclingConverter(
            source_file=self.source_file,
            markdown_file=self.markdown_file,
            images_dir=self.images_dir,
        )

    def test_init_sets_attributes(self) -> None:
        """Test that initialization sets all attributes correctly."""
        assert self.converter.source_file == self.source_file
        assert self.converter.markdown_file == self.markdown_file
        assert self.converter.images_dir == self.images_dir

    def test_validate_document_file_not_exists(self) -> None:
        """Test validate_document returns False for non-existent file."""
        file: Path = Path("/tmp/nonexistent.docx")
        converter: DoclingConverter = type(self.converter)(file, self.markdown_file, self.images_dir)
        assert not converter.validate_document([".docx", ".pdf"])

    def test_validate_document_unsupported_extension(self, tmp_path: Path) -> None:
        """Test validate_document returns False for unsupported file extension.

        Args:
            tmp_path: Temporary directory provided by pytest.
        """
        file: Path = tmp_path / "test.txt"
        file.write_text("text")
        converter: DoclingConverter = type(self.converter)(file, self.markdown_file, self.images_dir)
        assert not converter.validate_document([".docx", ".pdf"])

    def test_validate_document_supported_extension(self, tmp_path: Path) -> None:
        """Test validate_document returns True for supported file extension.

        Args:
            tmp_path: Temporary directory provided by pytest.
        """
        file: Path = tmp_path / "test.docx"
        file.write_text("text")
        converter: DoclingConverter = type(self.converter)(file, self.markdown_file, self.images_dir)
        assert converter.validate_document([".docx", ".pdf"])

    @patch("rag_assistant.document_preprocessor.DocumentConverter")
    @patch("rag_assistant.file_service.FileService.write_text")
    def test_docling_process_document_success(
        self,
        mock_write_text: MagicMock,
        mock_document_converter: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test docling_process_document writes markdown on success.

        Args:
            mock_write_text: Mock for FileService.write_text.
            mock_document_converter: Mock for DocumentConverter.
            tmp_path: Temporary directory provided by pytest.
        """
        file: Path = tmp_path / "test.docx"
        file.write_text("text")
        self.converter.source_file = file
        mock_converter_instance: MagicMock = MagicMock()
        mock_result: MagicMock = MagicMock()
        mock_result.document.export_to_markdown.return_value = "markdown content"
        mock_result.document = mock_result.document
        mock_converter_instance.convert.return_value = mock_result
        mock_document_converter.return_value = mock_converter_instance
        self.converter.docling_process_document()
        mock_converter_instance.convert.assert_called_once_with(file)
        mock_write_text.assert_called_once_with("markdown content", self.markdown_file)

    @patch("rag_assistant.document_preprocessor.DocumentConverter")
    def test_docling_process_document_failure(
        self, mock_document_converter: MagicMock, tmp_path: Path
    ) -> None:
        """Test docling_process_document raises RuntimeError on conversion failure.

        Args:
            mock_document_converter: Mock for DocumentConverter.
            tmp_path: Temporary directory provided by pytest.
        Raises:
            RuntimeError: If conversion fails.
        """
        file: Path = tmp_path / "test.docx"
        file.write_text("text")
        self.converter.source_file = file
        mock_converter_instance: MagicMock = MagicMock()
        mock_converter_instance.convert.side_effect = Exception("fail")
        mock_document_converter.return_value = mock_converter_instance
        with pytest.raises(RuntimeError):
            self.converter.docling_process_document()

    @patch("rag_assistant.document_preprocessor.DocumentConverter")
    def test_docling_process_document_no_document(
        self, mock_document_converter: MagicMock, tmp_path: Path
    ) -> None:
        """Test docling_process_document raises RuntimeError if no document is returned.

        Args:
            mock_document_converter: Mock for DocumentConverter.
            tmp_path: Temporary directory provided by pytest.
        Raises:
            RuntimeError: If no document is returned.
        """
        file: Path = tmp_path / "test.docx"
        file.write_text("text")
        self.converter.source_file = file
        mock_converter_instance: MagicMock = MagicMock()
        mock_result: MagicMock = MagicMock()
        mock_result.document = None
        mock_converter_instance.convert.return_value = mock_result
        mock_document_converter.return_value = mock_converter_instance
        with pytest.raises(RuntimeError):
            self.converter.docling_process_document()

    @patch("rag_assistant.file_service.FileService.read_lines")
    @patch("rag_assistant.file_service.FileService.write_text")
    def test_clean_markdown_file(
        self, mock_write_text: MagicMock, mock_read_lines: MagicMock
    ) -> None:
        """Test clean_markdown_file processes and writes cleaned markdown.

        Args:
            mock_write_text: Mock for FileService.write_text.
            mock_read_lines: Mock for FileService.read_lines.
        """
        lines = [
            "# Heading\n",
            "Some text\n",
            "| Col1 | Col2 |\n",
            "|------|------|\n",
            "Row1 | Row2\n",
            "\n",
            "- item1\n",
            "- item2\n",
            "\n",
            "Another paragraph\n",
        ]
        mock_read_lines.return_value = lines
        self.converter.clean_markdown_file()
        args, kwargs = mock_write_text.call_args
        assert isinstance(args[0], str)
        assert args[1] == self.markdown_file

    @patch("rag_assistant.file_service.FileService.read_text")
    @patch("rag_assistant.file_service.FileService.write_text")
    def test_replace_image_placeholders_with_markdown(
        self, mock_write_text: MagicMock, mock_read_text: MagicMock
    ) -> None:
        """Test replace_image_placeholders_with_markdown writes markdown image links.

        Args:
            mock_write_text: Mock for FileService.write_text.
            mock_read_text: Mock for FileService.read_text.
        """
        mock_read_text.return_value = "Some text [IMAGE: img1.png] more text"
        self.converter.images_dir = "images"
        self.converter.replace_image_placeholders_with_markdown()
        args, kwargs = mock_write_text.call_args
        assert "![IMAGE](images/img1.png)" in args[0]
        assert args[1] == self.markdown_file


class TestUnstructuredConverter:
    def setup_method(self) -> None:
        """Set up the UnstructuredConverter instance for testing.

        Initializes the source, markdown, and JSON paths and the converter instance.
        """
        self.source_file: Path = Path("/tmp/source.docx")
        self.markdown_file: Path = Path("/tmp/test.md")
        self.json_file: Path = Path("/tmp/test.json")
        self.converter: UnstructuredConverter = UnstructuredConverter(
            source_file=self.source_file,
            markdown_file=self.markdown_file,
            json_file=self.json_file,
        )

    def test_init_sets_attributes(self) -> None:
        """Test that initialization sets all attributes correctly."""
        assert self.converter.source_file == self.source_file
        assert self.converter.markdown_file == self.markdown_file
        assert self.converter.json_file == self.json_file

    @patch("rag_assistant.document_preprocessor.partition")
    @patch("rag_assistant.file_service.FileService.write_json")
    def test_unstructured_process_markdown_success(
        self,
        mock_write_json: MagicMock,
        mock_partition: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test unstructured_process_markdown writes JSON on success.

        Args:
            mock_write_json: Mock for FileService.write_json.
            mock_partition: Mock for partition function.
            tmp_path: Temporary directory provided by pytest.
        """
        md_file: Path = tmp_path / "test.md"
        md_file.write_text("# Title\nContent")
        self.converter.markdown_file = md_file
        mock_element: MagicMock = MagicMock()
        mock_element.to_dict.return_value = {"type": "Title", "text": "Title"}
        mock_partition.return_value = [mock_element]
        self.converter.unstructured_process_markdown(strategy="fast")
        mock_partition.assert_called_once_with(filename=md_file, strategy="fast")
        mock_write_json.assert_called_once_with(
            [{"type": "Title", "text": "Title"}], self.json_file
        )

    def test_unstructured_process_markdown_file_not_found(self) -> None:
        """Test unstructured_process_markdown raises FileNotFoundError for missing file.

        Raises:
            FileNotFoundError: If markdown file does not exist.
        """
        self.converter.markdown_file = Path("/tmp/nonexistent.md")
        with pytest.raises(FileNotFoundError):
            self.converter.unstructured_process_markdown()

    @patch("rag_assistant.document_preprocessor.partition")
    @patch("rag_assistant.file_service.FileService.write_json")
    def test_unstructured_process_markdown_strategy_argument(
        self,
        mock_write_json: MagicMock,
        mock_partition: MagicMock,
        tmp_path: Path,
    ) -> None:
        """Test unstructured_process_markdown passes strategy argument to partition.

        Args:
            mock_write_json: Mock for FileService.write_json.
            mock_partition: Mock for partition function.
            tmp_path: Temporary directory provided by pytest.
        """
        md_file: Path = tmp_path / "test.md"
        md_file.write_text("# Title\nContent")
        self.converter.markdown_file = md_file
        mock_partition.return_value = []
        self.converter.unstructured_process_markdown(strategy="ocr_only")
        mock_partition.assert_called_once_with(filename=md_file, strategy="ocr_only")


class TestEnrichment:
    def setup_method(self) -> None:
        """Set up the Enrichment instance and mocks for testing.

        Initializes the mock OpenAI client and enrichment instance.
        """
        self.mock_client: MagicMock = MagicMock()
        self.mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="AI válasz"))
        ]
        self.mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = "AI válasz"
        self.source_file: Path = Path("/tmp/source.docx")
        self.json_file: Path = Path("/tmp/test.json")
        self.enriched_json_file: Path = Path("/tmp/enriched.json")
        self.enrichment: Enrichment = Enrichment(
            source_file=self.source_file,
            json_file=self.json_file,
            client=self.mock_client,
            enriched_json_file=self.enriched_json_file,
        )

    def test_call_openai_api(self) -> None:
        """Test call_openai_api returns expected response."""
        result: str = self.enrichment.call_openai_api("gpt-model", "prompt", "system")
        assert result == "AI válasz"

    def test_call_openai_vision_api(self) -> None:
        """Test call_openai_vision_api returns expected vision response."""
        self.mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = "Vision válasz"
        result: str = self.enrichment.call_openai_vision_api("vision-model", "base64img")
        assert result == "Vision válasz"

    @patch(
        "rag_assistant.file_service.FileService.encode_image_base64",
        return_value="base64img",
    )
    def test_summarize_image(self, mock_encode: MagicMock) -> None:
        """Test summarize_image returns expected image description.

        Args:
            mock_encode: Mock for encode_image_base64.
        """
        self.mock_client.chat.completions.create.return_value.choices[
            0
        ].message.content = "Kép leírás"
        result: str = self.enrichment.summarize_image("vision-model", "/tmp/image.png")
        assert result == "Kép leírás"

    @patch("rag_assistant.prompts.TABLE_SYSTEM_MESSAGE", new="system")
    @patch("rag_assistant.prompts.TABLE_SUMMARY_PROMPT", new="{table_data}")
    def test_summarize_table(self) -> None:
        """Test summarize_table returns expected table summary."""
        self.enrichment.call_openai_api = MagicMock(
            return_value="Táblázat összefoglaló"
        )
        result: str = self.enrichment.summarize_table("gpt-model", "<table></table>")
        assert result == "Táblázat összefoglaló"

    @patch(
        "rag_assistant.file_service.FileService.read_json",
        return_value=[
            {"type": "Table", "metadata": {"text_as_html": "<table></table>"}},
            {"type": "Image", "metadata": {"image_url": "/tmp/image.png"}},
            {"type": "Other", "metadata": {}},
        ],
    )
    @patch("rag_assistant.file_service.FileService.write_json")
    def test_enrich_json(
        self, mock_write_json: MagicMock, mock_read_json: MagicMock
    ) -> None:
        """Test enrich_json adds summaries to table and image elements.

        Args:
            mock_write_json: Mock for FileService.write_json.
            mock_read_json: Mock for FileService.read_json.
        """
        self.enrichment.summarize_table = MagicMock(
            return_value="Táblázat összefoglaló"
        )
        self.enrichment.summarize_image = MagicMock(return_value="Kép leírás")
        self.enrichment.enrich_json(
            process_table_with_ai=True,
            process_images_with_ai=True,
            text_model="gpt-model",
            image_model="vision-model",
        )
        args = mock_write_json.call_args[0][0]
        assert args[0]["metadata"]["table_summary"] == "Táblázat összefoglaló"
        assert args[1]["metadata"]["image_description"] == "Kép leírás"


class TestExport:
    def test_export_init(self, tmp_path: Path) -> None:
        """Test that Export initialization sets all attributes correctly.

        Args:
            tmp_path: Temporary directory provided by pytest.
        """
        json_file: Path = tmp_path / "test.json"
        txt_file: Path = tmp_path / "test.txt"
        export: Export = Export(enriched_json_file=str(json_file), txt_file=str(txt_file))
        assert export.enriched_json_file == str(json_file)
        assert export.txt_file == str(txt_file)

    def test_export_text_from_enriched_json_table_and_image(self, tmp_path: Path) -> None:
        """Test export_text_from_enriched_json writes all expected content.

        Args:
            tmp_path: Temporary directory provided by pytest.
        """
        json_file: Path = tmp_path / "test.json"
        txt_file: Path = tmp_path / "test.txt"
        elements = [
            {"metadata": {"table_summary": "Összefoglaló táblázat"}},
            {"metadata": {"image_description": "Kép leírása"}},
            {"text": "Csak szöveg"},
            {"metadata": {}, "text": "Szöveg meta nélkül"},
        ]
        json_file.write_text(json.dumps(elements, ensure_ascii=False))
        export: Export = Export(enriched_json_file=str(json_file), txt_file=str(txt_file))
        export.export_text_from_enriched_json()
        output: str = txt_file.read_text()
        assert "Összefoglaló táblázat" in output
        assert "Kép leírása" in output
        assert "Csak szöveg" in output
        assert "Szöveg meta nélkül" in output

    def test_export_text_from_enriched_json_file_not_found(self, tmp_path: Path) -> None:
        """Test export_text_from_enriched_json raises FileNotFoundError if file is missing.

        Args:
            tmp_path: Temporary directory provided by pytest.
        Raises:
            FileNotFoundError: If the enriched JSON file does not exist.
        """
        json_file: Path = tmp_path / "notfound.json"
        txt_file: Path = tmp_path / "test.txt"
        export: Export = Export(enriched_json_file=str(json_file), txt_file=str(txt_file))

        with pytest.raises(FileNotFoundError):
            export.export_text_from_enriched_json()
