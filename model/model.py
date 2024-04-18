import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.util import ngrams
from model.vsm import vsm
from model.bert import bert
import shutil

def standard_tokenize(quotes_dictionary):
    # Create a new dictionary to store tokenized quotes
    tokenized_quotes = {}

    # Tokenize quotes for each author
    for author, quotes in quotes_dictionary.items():
        # Tokenize each quote for the author
        tokenized_quotes[author] = [word_tokenize(quote) for quote in quotes]

    return tokenized_quotes

def stem_and_tokenize(quotes_dictionary):
    # Create a new dictionary to store tokenized and stemmed quotes
    tokenized_and_stemmed_quotes = {}
    stemmer = PorterStemmer()

    # Tokenize and stem quotes for each author
    for author, quotes in quotes_dictionary.items():
        tokenized_and_stemmed_quotes[author] = []
        # Tokenize each quote for the author and then stem the tokens
        for quote in quotes:
            tokens = word_tokenize(quote)
            stemmed_tokens = [stemmer.stem(token) for token in tokens]
            tokenized_and_stemmed_quotes[author].append(stemmed_tokens)

    return tokenized_and_stemmed_quotes

def bigram_tokenize(quotes_dictionary):
    # Create a new dictionary to store bigram tokenized quotes
    bigram_tokenized_quotes = {}

    # Tokenize quotes for each author
    for author, quotes in quotes_dictionary.items():
        # Tokenize each quote for the author into bigrams
        for quote in quotes:
            quote = '<START> ' + quote + ' <END>'
            quotes_list = bigram_tokenized_quotes.get(author, [])
            quotes_list.append([' '.join(bigram) for bigram in ngrams(quote.split(), 2)])
            bigram_tokenized_quotes[author] = quotes_list
    return bigram_tokenized_quotes

def get_quotes(folder):
    quotes_dict = {}

    # Iterate over files in the folder
    for filename in os.listdir(folder):
        # Extract author name from filename
        author = os.path.splitext(filename)[0]

        # Initialize list of quotes for the author
        quotes_dict[author] = []

        # Read quotes from file and append to quotes list
        with open(os.path.join(folder, filename), 'r') as file:
            for line in file:
                quotes_dict[author].append(line.strip())

    return quotes_dict

def do_vsm(training_tokens_dictionary, testing_tokens_dictionary, out_folder, tokenization):

    # Do our vector space model with all 9 different weighting schemes
    print()
    print(f"doing vector space with {tokenization} tfc tfx")
    tfc_tfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'tfc', 'tfx')

    with open(os.path.join(out_folder, f"{tokenization}_tfc_tfx.txt"), 'w') as out_file:
        out_file.write(str(tfc_tfx))

    print()
    print(f"doing vector space with {tokenization} tfx nfx")
    tfx_nfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'tfx', 'nfx')

    with open(os.path.join(out_folder, f"{tokenization}_tfx_nfx.txt"), 'w') as out_file:
        out_file.write(str(tfx_nfx))

    print()
    print(f"doing vector space with {tokenization} txc nfx")
    txc_nfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'txc', 'nfx')

    with open(os.path.join(out_folder, f"{tokenization}_txc_nfx.txt"), 'w') as out_file:
        out_file.write(str(txc_nfx))

    print()
    print(f"doing vector space with {tokenization} tfx tfx")
    tfx_tfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'tfx', 'tfx')

    with open(os.path.join(out_folder, f"{tokenization}_tfx_tfx.txt"), 'w') as out_file:
        out_file.write(str(tfx_tfx))

    print()
    print(f"doing vector space with {tokenization} nxx bpx")
    nxx_bpx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'nxx', 'bpx')

    with open(os.path.join(out_folder, f"{tokenization}_nxx_bpx.txt"), 'w') as out_file:
        out_file.write(str(nxx_bpx))

    print()
    print(f"doing vector space with {tokenization} bfx bfx")
    bfx_bfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'bfx', 'bfx')

    with open(os.path.join(out_folder, f"{tokenization}_bfx_bfx.txt"), 'w') as out_file:
        out_file.write(str(bfx_bfx))

    print()
    print(f"doing vector space with {tokenization} bxx bpx")
    bxx_bpx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'bxx', 'bpx')

    with open(os.path.join(out_folder, f"{tokenization}_bxx_bpx.txt"), 'w') as out_file:
        out_file.write(str(bxx_bpx))

    print()
    print(f"doing vector space with {tokenization} txc txx")
    txc_txx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'txc', 'txx')

    with open(os.path.join(out_folder, f"{tokenization}_txc_txx.txt"), 'w') as out_file:
        out_file.write(str(txc_txx))

    print()
    print(f"doing vector space with {tokenization} bxx bxx")
    bxx_bxx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'bxx', 'bxx')

    with open(os.path.join(out_folder, f"{tokenization}_bxx_bxx.txt"), 'w') as out_file:
        out_file.write(str(bxx_bxx))

def model():
    print("--- Making predictions! ---")

    train_folder_path = 'TVShowQuotes-Train'
    # {author: [quote]}
    train_quotes_dictionary = get_quotes(train_folder_path)
    # {author: [[quote tokens]]}

    test_folder_path = 'TVShowQuotes-Test'
    test_quotes_dictionary = get_quotes(test_folder_path)

    out_folder = "predictions"
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.makedirs(out_folder)

    # Tokenized with NLTK
    standard_training_tokens_dictionary = standard_tokenize(train_quotes_dictionary)
    standard_testing_tokens_dictionary = standard_tokenize(test_quotes_dictionary)

    do_vsm(standard_training_tokens_dictionary, standard_testing_tokens_dictionary, out_folder, "standard")

    # Tokenized and Stemmed with NLTK and PorterStemmer
    stemmed_training_tokens_dictionary = stem_and_tokenize(train_quotes_dictionary)
    stemmed_testing_tokens_dictionary = stem_and_tokenize(test_quotes_dictionary)

    do_vsm(stemmed_training_tokens_dictionary, stemmed_testing_tokens_dictionary, out_folder, "stemmed")

    # tokenized into bigrams
    bigram_training_tokens_dictionary = bigram_tokenize(train_quotes_dictionary)
    bigram_testing_tokens_dictionary = bigram_tokenize(test_quotes_dictionary)

    do_vsm(bigram_training_tokens_dictionary, bigram_testing_tokens_dictionary, out_folder, "bigram")

    # print()
    # print("training bert model to make predictions")
    # bert_predictions = bert(train_quotes_dictionary, test_quotes_dictionary)

    # with open(os.path.join(out_folder, "bert.txt"), 'w') as out_file:
    #     out_file.write(str(bert_predictions))

    return
