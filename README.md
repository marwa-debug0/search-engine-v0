## Log 1:
Added the document processing module : normalize, tokenize, remove stop words and stem
Used NLTK library for the stopwords and the porter stemmer : https://www.nltk.org/index.html
The main function takes two jsonl file paths as an input and processes each document in the first file, then writes the processed document in the other jsonl file.

## Log 2:
Added the index processing module : build the inverted index from the processed documents and save it as a json file

## Log 3 : 
Added the query processing module : takes a query as an input and processes it then returns the processed tokens

## Log 4: 
Added the ranking processing module : builds the ranking system using the cosine similarity
