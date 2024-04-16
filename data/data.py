import pandas as pd
import os
import shutil
import random

def get_quotes_for_person(data, person):
    """Extract quotes for a given person from the dataset."""
    person_data = data[data['Character'] == person]
    return list(person_data['Dialogue'].dropna())

def write_quotes_to_files(person, quotes):
    """Write quotes to train and test files."""
    random.shuffle(quotes)  # Shuffle the quotes randomly

    # Calculate the number of quotes to put in the test set (10% of the total quotes)
    num_test_quotes = len(quotes) // 10

    # Divide the quotes into train and test sets
    train_quotes = quotes[num_test_quotes:]
    test_quotes = quotes[:num_test_quotes]

    # Write the train quotes to their files in the quotes folder
    folder = 'quotes'
    train_filename = os.path.join(folder, f"{person.replace(' ', '_')}.txt")
    with open(train_filename, 'w', encoding='utf-8') as train_file:
        for quote in train_quotes:
            train_file.write(quote + '\n')

    # Write the test quotes to their files in the test-quotes folder
    test_folder = 'test-quotes'
    test_filename = os.path.join(test_folder, f"{person.replace(' ', '_')}.txt")
    with open(test_filename, 'w', encoding='utf-8') as test_file:
        for quote in test_quotes:
            test_file.write(quote + '\n')

def data():
    csv_file_path = "seinfeld_quotes.csv"
    
    # Load the CSV file
    seinfeld_data = pd.read_csv(csv_file_path)

    # Reset data folders
    folder = 'quotes'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    test_folder = 'test-quotes'
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)
    os.makedirs(test_folder)

    # Get list of people
    people = seinfeld_data['Character'].dropna().unique()

    # Process quotes for each person
    for person in people:
        quotes = get_quotes_for_person(seinfeld_data, person)
        if quotes:
            print(f"Writing quotes for {person} to file...")
            write_quotes_to_files(person, quotes)
            print(f"Quotes for {person} written to {person.replace(' ', '_')}.txt")
            print()
        else:
            print(f"No quotes found for {person}")
            print()

    # Write all characters to people.txt
    with open('data/people.txt', 'w', encoding='utf-8') as file:
        for person in sorted(people):
            file.write(person + '\n')