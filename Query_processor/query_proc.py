import sys
from pathlib import Path

# Add project root to sys.path so Document_processor can be found when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Document_processor.doc_proc import process_document

def process_query(query):
    processed_tokens = process_document(query)

    return processed_tokens
