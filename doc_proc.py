import json
import re

from nltk.corpus import stopwords

# Porter stemmer algorithm 
from nltk.stem import PorterStemmer


INPUT_PATH = "wiki.jsonl"
OUTPUT_PATH = "processed_wiki.jsonl"

# Fields in the wiki.jsonl 
ID_FIELD = "id"
URL_FIELD = "url"
TITLE_FIELD = "title"
TEXT_FIELD = "text"

# We use a set because its efficient 
STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()

def normalize_text(text) :
    text = text.lower()
    # Replaces consecutive spaces with one space
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# Removes punctuation but the text should be normalized first because it won't detect uppercases 
def tokenize_text(text) :
    tokens = re.findall(r"[a-z0-9]+", text)

    return tokens


# Normalize -> Tokenize -> Remove stop words -> Stem
def process_document(text):

    text = normalize_text(text)
    tokens = tokenize_text(text)

    processed_tokens = []

    for token in tokens:
        if token in STOP_WORDS:
            continue

        # Convert the word into its stem
        stemmed_token = STEMMER.stem(token)
        processed_tokens.append(stemmed_token)
    
    return processed_tokens


def process_corpus(INPUT_PATH, OUTPUT_PATH):
    processed_count = 0
    skipped_count = 0

    with open(INPUT_PATH, "r", encoding="UTF-8") as infile, open(OUTPUT_PATH, "w", encoding="UTF-8") as outfile :
        for line_number, line in enumerate(infile, 1):
            try :
                doc = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON at line {line_number}")
                skipped_count += 1
                continue

            #Extracting document fields 
            doc_id = doc.get(ID_FIELD, line_number)
            url = doc.get(URL_FIELD, "")
            title = doc.get(TITLE_FIELD, "")
            raw_text = doc.get(TEXT_FIELD, "")

            #Process the article 
            tokens = process_document(raw_text)

            #Build the processed document 
            processed_doc = {
                "id": doc_id,
                "url": url,
                "title": title,
                "tokens": tokens
            }

            #Write the processed jsonl
            outfile.write(json.dumps(processed_doc, ensure_ascii=False) + "\n")
            processed_count += 1

        print("\nProcessing complete!")
        print(f"Documents processed: {processed_count}")
        print(f"Invalid documents skipped: {skipped_count}")













