import os
import nltk
from nltk.tokenize import word_tokenize
from model.vsm import vsm
import shutil

def tokenize(quotes_dictionary):
    # Create a new dictionary to store tokenized quotes
    tokenized_quotes = {}

    # Tokenize quotes for each author
    for author, quotes in quotes_dictionary.items():
        # Tokenize each quote for the author
        tokenized_quotes[author] = [word_tokenize(quote) for quote in quotes]

    return tokenized_quotes

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


def model():
    print("--- Making predictions! ---")

    train_folder_path = 'TVShowQuotes-Train'
    # {author: [quote]}
    train_quotes_dictionary = get_quotes(train_folder_path)
    # {author: [[quote tokens]]}
    training_tokens_dictionary = tokenize(train_quotes_dictionary)

    test_folder_path = 'TVShowQuotes-Test'
    test_quotes_dictionary = get_quotes(test_folder_path)
    testing_tokens_dictionary = tokenize(test_quotes_dictionary)

    print()
    print("doing vector space with tfc tfx")
    tfc_tfx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'tfc', 'tfx')

    out_folder = "predictions"
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.makedirs(out_folder)

    with open(os.path.join(out_folder, "tfc_tfx.txt"), 'w') as out_file:
        out_file.write(str(tfc_tfx))

    print()
    print("doing vector space with bxx bxx")
    bxx_bxx = vsm(training_tokens_dictionary, testing_tokens_dictionary, 'bxx', 'bxx')

    with open(os.path.join(out_folder, "bxx_bxx.txt"), 'w') as out_file:
        out_file.write(str(bxx_bxx))

    return
