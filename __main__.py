from rank_proc import load_document_metadata
from query_proc import process_query
from rank_proc import INDEX_PATH
from rank_proc import load_index, count_documents, calculate_idf, calculate_document_norms, rank_documents

query = "How to print a string in python?"

INDEX = load_index("inverted_index.json")
total_documents = count_documents("processed_wiki.jsonl")

# Calculate IDF and document norms once.
idf = calculate_idf(INDEX, total_documents)
document_norms = calculate_document_norms(INDEX, idf)

query_tokens = process_query(query)
metadata = load_document_metadata("processed_wiki.jsonl")

results = rank_documents(
    query_tokens,
    INDEX,
    idf,
    document_norms,
    top_k=5
)

print("\nTop search results:")

for doc_id, score in results:
    doc_meta = metadata.get(doc_id, {})
    print(f"Document: {doc_id} | Score: {score:.4f}")
    print(f"Title: {doc_meta.get('title', 'N/A')}")
    print(f"URL: {doc_meta.get('url', 'N/A')}")
    print("-" * 30)
