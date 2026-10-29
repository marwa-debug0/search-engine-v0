# Transform every document to a vector 
import json
import math
from collections import defaultdict, Counter

INDEX_PATH = "inverted_index.json"
PROCESSED_DOCS_PATH = "processed_wiki.jsonl"

def load_index(index_path):
    with open(index_path, "r", encoding = "UTF-8") as infile:
        return json.load(infile)

def count_documents(processed_path):
    count = 0

    with open(processed_path, "r", encoding="UTF-8") as infile:
        for line in infile:
            if line.strip():
                count += 1

    return count


INDEX = load_index(INDEX_PATH)
NUM_DOCS = count_documents(PROCESSED_DOCS_PATH)

def calculate_doc_frequency(index):
    df = {}
    for term, posting in index.items():
        df[term] = len(posting)
    
    return df 


def calculate_idf(index, num_docs=NUM_DOCS):
    document_frequencies = calculate_doc_frequency(index)
    idf = {}
    for term, df_score in document_frequencies.items():
        idf [term] = math.log10(num_docs / df_score)
    return idf 

def calculate_doc_norms(index, idf):
    squared_norms = defaultdict(float)
    for term, posting in index.items():
        idf_term = idf[term]
        for doc_id, tf in posting.items():
            weight = idf_term * tf 
            squared_norms[doc_id] += weight ** 2
        
    return {doc_id: math.sqrt(value) for doc_id, value in squared_norms.items()}

def calculate_query_vector(query_tokens, idf):
    query_tf = Counter(query_tokens)
    query_vector = {}
    for term, tf in query_tf.items():
        # We can't compare a query token that isn't in our index 
        
        if term in idf: 
            query_vector[term] = idf[term] * tf 
    
    return query_vector

def rank_documents(query_tokens, index, idf, document_norms, top_k = 5):
    query_vector = calculate_query_vector(query_tokens, idf)
    if not query_vector:
        return []
    
    # Calculate the query's L2 norm 
    query_norm = math.sqrt(sum(w*w for w in query_vector.values()))

    # Candidate docs 
    candidate_docs = set()

    for term in query_vector:
        for doc_id in index[term]:
            candidate_docs.add(doc_id)

    
    scores = {}
    # Calculate the cosine simalarity of the query and docs
    for doc_id in candidate_docs:
        dot_product = 0

        for term, query_weight in query_vector.items():
            posting = index[term]

            if doc_id in posting:
                tf = posting[doc_id]
                doc_weight = tf * idf[term]

                dot_product += query_weight * doc_weight
            
        
        doc_norm = document_norms.get(doc_id, 0)

        if doc_norm == 0 or query_norm == 0: 
            continue
        
        similarity = dot_product / (doc_norm * query_norm)
        scores[doc_id] = similarity

    
    ranked_docs = sorted(scores.items(), key= lambda item : item[1], reverse = True)

    return ranked_docs [: top_k]


calculate_document_norms = calculate_doc_norms


def load_document_metadata(processed_path):
    """Load document titles and URLs, indexed by document ID."""
    metadata = {}

    with open(processed_path, "r", encoding="utf-8") as infile:
        for line in infile:
            if not line.strip():
                continue

            doc = json.loads(line)
            doc_id = str(doc["id"])

            metadata[doc_id] = {
                "title": doc.get("title", "Untitled"),
                "url": doc.get("url", "")
            }

    return metadata
        





    

    
    
    




    


    
    