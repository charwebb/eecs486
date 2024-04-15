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
            if docSchema[0] == 't':
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

# Added parameter docCount = N, since I already iterate through each document in main
def retrieveDocuments(query, invertedIndex, docScheme, queryScheme, docCount):

    # get relevant documents and store as as set.
    relevantDocuments = set()
    queryFrequencies = {}
    for word in query:

        # query term frequency
        # tf
        if queryScheme[0] == 't':
            queryFrequencies[word] = queryFrequencies.get(word, 0) + 1
        # 1
        elif queryScheme[0] == 'b':
            queryFrequencies[word] = queryFrequencies.get(word, 1)

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

            queryVector[term] = frequency * idf

    # get the length of all document vectors and the length of the query vector
    if docScheme[2] == 'c':
        docLengths = getDocVectorLengths(invertedIndex, docCount, docScheme)

    # query cosine similarity normalization
    # 1
    if queryScheme[2] == 'x':
        queryLength = 1
    # c: length of vector
    else:
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
                    else:
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


def vsm(tokens, test_tokens, docSchemas, querySchemas):
    # run with python3 vectorspace.py tfc tfx cranfieldDocs/ cranfield.queries
    # or with python3 vectorspace.py bxx bxx cranfieldDocs/ cranfield.queries

    # {term: [term frequency, {document, document_frequency}]}
    invertedIndex = {}

    docCount = 0
    for author, quotes in tokens.items():
        docCount += len(quotes)
        document = (author, quotes)
        invertedIndex = indexDocument(document, docSchemas, invertedIndex)

    # {author: retrieved documents}
    queriedDocuments = {}

    # {author: correct documents}
    # (correct documents is just the author because we want to retrieve THE author of the quote)
    correctDocuments = {}

    for author, quotes in test_tokens.items():
        correctDocuments[author] = [author]
        queryid = author
        for quote in quotes:
            queriedDocuments[queryid] = retrieveDocuments(quote, invertedIndex, docSchemas, querySchemas, docCount)

    # calculate macro-averaged precision and recall, print to command line

    def precision(queryid, queriedDocuments, correctDocuments):
        retrieved_documents = set([docid for docid, _ in queriedDocuments.get(queryid, [])])
        relevant_documents = set(docid for docid in correctDocuments.get(queryid, []))

        if len(retrieved_documents) == 0:
            return 0

        truePositives = len(retrieved_documents.intersection(relevant_documents))
        return truePositives / len(retrieved_documents)

    def recall(queryid, queriedDocuments, correctDocuments):
        retrieved_documents = set([docid for docid, _ in queriedDocuments.get(queryid, [])])
        relevant_documents = set(docid for docid in correctDocuments.get(queryid, []))

        if len(relevant_documents) == 0:
            return 0

        truePositives = len(retrieved_documents.intersection(relevant_documents))
        return truePositives / len(relevant_documents)

    def macro_averaged_precision_recall(queriedDocuments, correctDocuments):
        totalPrecision = 0
        totalRecall = 0
        numQueries = len(queriedDocuments)

        for queryid in queriedDocuments.keys():
            totalPrecision += precision(queryid, queriedDocuments, correctDocuments)
            totalRecall += recall(queryid, queriedDocuments, correctDocuments)

        macroPrecision = totalPrecision / numQueries
        macroRecall = totalRecall / numQueries

        return macroPrecision, macroRecall

    def calculate_accuracy(queriedDocuments):
        correct_count = 0
        total_count = 0

        for author, retrieved_docs in queriedDocuments.items():
            # Check if there are any retrieved documents for the author
            if retrieved_docs:
                # Get the top-ranked document for the author
                top_ranked_author = retrieved_docs[0][0]

                # Check if the top-ranked document matches the correct author
                if top_ranked_author == author:
                    correct_count += 1

                total_count += 1

        # Calculate accuracy
        if total_count > 0:
            accuracy = correct_count / total_count
        else:
            accuracy = 0.0

        return accuracy

    macroPrecision, macroRecall = macro_averaged_precision_recall(queriedDocuments, correctDocuments)

    accuracy = calculate_accuracy(queriedDocuments)

    print("Perfectly accurate predictions:", accuracy)
    print("Macro-averaged Precision:", macroPrecision)
    print("Macro-averaged Recall:", macroRecall)


