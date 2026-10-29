import sys
from pathlib import Path

# Add project root to sys.path so sibling packages (Document_processor) can be resolved
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Query_processor.query_proc import process_query

query = "How to reverse a linked list in Python?"

processed_query = process_query(query)
print(processed_query)