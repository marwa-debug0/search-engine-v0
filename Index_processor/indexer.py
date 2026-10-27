# We will implement a simple indexer with terms as keys and (document ID, term frequency) as the value


import json
from collections import defaultdict

INPUT_PATH = "processed_wiki.jsonl"
OUTPUT_PATH = "inverted_index.json"


def build_index(input_path):
    inverted_index = defaultdict(lambda: defaultdict(int))

    with open(input_path, "r", encoding="utf-8") as infile:
        for line in infile:
            if not line.strip():
                continue

            doc = json.loads(line)
            doc_id = doc["id"]
            doc_tokens = doc["tokens"]

            for term in doc_tokens:
                inverted_index[term][doc_id] += 1

    # Convert defaultdicts into ordinary dictionaries
    return {
        term: dict(postings)
        for term, postings in inverted_index.items()
    }


def save_index(index, output_path):
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(index, outfile, ensure_ascii=False)


