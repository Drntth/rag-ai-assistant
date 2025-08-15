import os
import sys

from document_preprocessor import DocumentPreProcessor

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    import config
except ImportError:
    config = None


def main():
    data_dir = getattr(config, "DATA_DIR", "data")
    input_filename = getattr(config, "INPUT_FILENAME", "test.docx")
    # api_key = getattr(config, 'API_KEY', None)
    # api_provider = getattr(config, 'API_PROVIDER', 'openai')

    processor = DocumentPreProcessor(
        data_dir=data_dir,
        steps=6,
        remove_headers=True,
        remove_footers=True,
        remove_toc=True,
        remove_empty=True,
        abbreviation_strategy="inline",
        footnote_handling="remove",
        process_table_with_ai=False,
        process_images_with_ai=False,
        # api_key=api_key,
        # api_provider=api_provider
    )
    processor.run(input_filename)


if __name__ == "__main__":
    main()
