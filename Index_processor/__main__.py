from indexer import build_index
from indexer import save_index

index = build_index("processed_wiki.jsonl")
save_index(index, "inverted_index.json")

print("The inverted index is created.")
