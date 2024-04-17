# regular vector space model
# Charles Webb
# uniqname: charwebb
# For EECS 486: Information Retrieval W24

import sys
import os
from math import sqrt, log
import random

# removed parameter query weighting schema since query is processed in retrieveDocuments
def indexDocument(document, docSchema, invertedIndex):
    # tokenize using assignment 1 tokenizer
    author = document[0]
    quotes = document[1]

    for quote in quotes:
        for token in quote:
            # find this term in the inverted index, otherwise initialize
            entry = invertedIndex.get(token, [0, {}])
            if not entry[1].get(author):
                entry[0] += 1

            # document term frequency
            # tf
            if docSchema[0] == 't' or docSchema[0] == 'n':
                entry[1][author] = entry[1].get(author, 0) + 1
            # 1
            elif docSchema[0] == 'b':
                entry[1][author] = entry[1].get(author, 1)

            # save the inverted index
            invertedIndex[token] = entry

    return invertedIndex

# return the lengths of each document as {docid: length} to be used in normalization
def getDocVectorLengths(invertedIndex, numDocuments, docScheme):
    docLengths = {}
    for term in invertedIndex:
        df = invertedIndex[term][0]
        # document document frequency #1
        # idf
        if docScheme[1] == 'f':
            idf = log(numDocuments / float(df))
        # 1
        elif docScheme[1] == 'x':
            idf = 1
        elif docScheme[1] == 'p':
            idf = log((numDocuments - float(df))/float(df))
        tokens = invertedIndex[term][1]
        for token in tokens:
            docid = token
            # document tf will already be 1 in inverted index here
            tf = float(tokens[token])
            docLengths[docid] = docLengths.get(docid, 0) + ((tf * idf) ** 2)

    for doc in docLengths:
        docLengths[doc] = sqrt(docLengths[doc])

    return docLengths

# returns the query vector length as an into to be used in normalization
def getQueryVectorLength(query):
    return sqrt(sum(value ** 2 for value in query.values()))

def cosineSimilarity(querytfidf, documenttfidf, queryNorm, documentNorm):
    product = querytfidf * documenttfidf
    if queryNorm == 0 or documentNorm == 0:
        return 0
    return product / (queryNorm * documentNorm)

def normalize_term_frequency_query(queryFrequencies):
    max_tf = max(queryFrequencies.values())

    for term, tf in queryFrequencies.items():
        normalized_tf = 0.5 + 0.5 * (tf / max_tf)
        queryFrequencies[term] = normalized_tf

    return queryFrequencies

# Added parameter docCount = N, since I already iterate through each document in main
def retrieveDocuments(query, invertedIndex, docScheme, queryScheme, docCount, cosineSimNormDocVectorLengths):

    # get relevant documents and store as as set.
    relevantDocuments = set()
    queryFrequencies = {}
    for word in query:

        # query term frequency
        # tf
        if queryScheme[0] == 't' or queryScheme[0] == 'n':
            queryFrequencies[word] = queryFrequencies.get(word, 0) + 1
        # 1
        elif queryScheme[0] == 'b':
            queryFrequencies[word] = queryFrequencies.get(word, 1)

    # Do an extra loop to normalize the term frequencies of the query.
    if queryScheme[0] == 'n':
        normalize_term_frequency_query(queryFrequencies)

    for word in queryFrequencies:
        if invertedIndex.get(word):
            for document in invertedIndex.get(word)[1]:
                relevantDocuments.add(document)

    # Calculate TF-IDF weighted query vector
    queryVector = {}
    for term, frequency in queryFrequencies.items():
        if term in invertedIndex:
            df = invertedIndex[term][0]
            # query document frequency
            # idf
            if queryScheme[1] == 'f':
                idf = log(docCount / (df))
            # 1
            elif queryScheme[1] == 'x':
                idf = 1
            elif queryScheme[1] == 'p':
                idf = log((docCount - float(df))/float(df))

            queryVector[term] = frequency * idf

    # get the length of all document vectors and the length of the query vector
    if docScheme[2] == 'c':
        docLengths = cosineSimNormDocVectorLengths

    # query cosine similarity normalization
    # 1
    if queryScheme[2] == 'x':
        queryLength = 1
    # c: length of vector
    elif queryScheme[2] == 'c':
        queryLength = getQueryVectorLength(queryVector)

    # get similaritiy scores using cosing similarity
    similarityScores = {}
    for word, querytfidf in queryVector.items():
        if word in invertedIndex:
            documents = invertedIndex[word][1]
            for docid, freq in documents.items():
                if docid in relevantDocuments:
                    # document document frequency
                    # idf
                    if docScheme[1] == 'f':
                        doctfidf = freq * log(docCount / (invertedIndex[word][0] + 1))
                    # 1
                    elif docScheme[1] == 'x':
                        doctfidf = freq

                    # document cosine similarity normalization
                    # x: 1
                    if docScheme[2] == 'x':
                        documentNormalization = 1
                    # c: length of vector
                    elif docScheme[2] == 'c':
                        documentNormalization = docLengths[docid]

                    similarity = cosineSimilarity(querytfidf, doctfidf, queryLength, documentNormalization)
                    similarityScores[docid] = similarityScores.get(docid, 0) + similarity

    # CHANGE THIS TO CHANGE HOW MANY DOCUMENTS YOU GET PER QUERY
    length = 10

    # add in random (literally random) new docid's until we have the desired amount
    while len(similarityScores) < length:
        randomDocId = random.randint(0, docCount)
        if randomDocId not in similarityScores:
            similarityScores[randomDocId] = 0.0

    # sort the scores by similarity score and return
    sortedScores = sorted(similarityScores.items(), key=lambda x: x[1], reverse=True)
    topScores = sortedScores[:length]
    return topScores

def normalize_term_frequency(inverted_index):
    max_tf = max(term_info[0] for term_info in inverted_index.values())

    for term, term_info in inverted_index.items():
        tf = term_info[0]
        normalized_tf = 0.5 + 0.5 * (tf / max_tf)
        inverted_index[term][0] = normalized_tf

    return inverted_index


def vsm(tokens, test_tokens, docSchemas, querySchemas):
    # run with python3 vectorspace.py tfc tfx cranfieldDocs/ cranfield.queries
    # or with python3 vectorspace.py bxx bxx cranfieldDocs/ cranfield.queries

    # {term: [term frequency, {document, document_frequency}]}
    invertedIndex = {}

    docCount = 0
    count = 0
    for author, quotes in tokens.items():
        docCount += len(quotes)
        document = (author, quotes)
        invertedIndex = indexDocument(document, docSchemas, invertedIndex)

    if docSchemas[0] == 'n':
        invertedIndex = normalize_term_frequency(invertedIndex)

    print("--- finished creating inverted index ---")

    # {author: retrieved documents}
    queriedDocuments = {}
    cosineSimNormDocVectorLengths = getDocVectorLengths(invertedIndex, docCount, docSchemas)
    # {author: correct documents}
    # (correct documents is just the author because we want to retrieve THE author of the quote)

    count = 0
    for author, quotes in test_tokens.items():
        print(f"retrieving relevant documents. Done {count}", end='\r')
        count += 1
        for quote in quotes:
            queriedDocuments[author] = retrieveDocuments(quote, invertedIndex, docSchemas, querySchemas, docCount, cosineSimNormDocVectorLengths)

    return queriedDocuments
