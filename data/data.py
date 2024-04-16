import requests
from bs4 import BeautifulSoup, Tag
import os
import shutil
import random
import pandas as pd
import re
import csv, sys

def data():
    seinfeldData()
    southParkData()
    officeData()
    return








def cleanCharacterColumn(name):
    name = re.sub(r'/.*|\(.*|&.*|\[.*', '', name)
    return name.strip().upper()

def seinfeldData():
    output_directory = 'TVShowQuotes'
    quotes_csv = 'seinfeld_quotes.csv'
    os.makedirs(output_directory, exist_ok=True)

    df = pd.read_csv(quotes_csv)
    df['Character'] = df['Character'].apply(cleanCharacterColumn)
    df['Dialogue'] = df['Dialogue'].astype(str)
    character_counts = df['Character'].value_counts().to_dict()
    character_counts = {k: v for k, v in character_counts.items() if k} # Removes all empties
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35} # Only keeps top occurances
    
    for character in top_character_counts:
            group = df[df['Character'] == character]
            # Filename for each character
            filename = os.path.join(output_directory, f"Seinfeld_{character.upper()}.txt")

            with open(filename, 'w', encoding='utf-8') as file:
                file.writelines(group['Dialogue'] + '\n')

    return

def southParkData():
    output_directory = 'TVShowQuotes'
    quotes_csv = 'southpark_quotes.csv'
    os.makedirs(output_directory, exist_ok=True)

    df = pd.read_csv(quotes_csv)
    df['Character'] = df['Character'].apply(cleanCharacterColumn)
    df['Line'] = df['Line'].astype(str)
    character_counts = df['Character'].value_counts().to_dict()
    character_counts = {k: v for k, v in character_counts.items() if k} # Removes all empties
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35} # Only keeps top occurances

    #print(top_character_counts)

    for character in top_character_counts:
        group = df[df['Character'] == character]
        filename = os.path.join(output_directory, f"SouthPark_{character.upper()}.txt")
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(group['Line'])
    return

def officeData():
    quotes_csv = 'office_quotes.csv'
    character_quotes = {}

    with open(quotes_csv, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            character = row['speaker']
            script = row['line_text']

            charList = character.split("/")
            for char in charList:
                if char in character_quotes:
                    character_quotes[char].append(script)
                else:
                    character_quotes[char] = []

        if(os.path.isdir("TVShowQuotes") == False):
            os.makedirs("TVShowQuotes")
        os.chdir("TVShowQuotes")

        for character in character_quotes:
            if(len(character_quotes[character]) > 35): # Only keeps top occurances
                newfile = f"Office_{character.upper()}.txt"
                with open(newfile, 'w') as output:
                    for quote in character_quotes[character]:
                        output.write(quote)
                        output.write("\n")

        return










# Old Charlie Code...
"""
def get_quotes_for_person(person):
    base_url = "https://en.wikiquote.org/wiki/"
    person_url = base_url + person.replace(" ", "_")

    # Make request to wikiquote
    response = requests.get(person_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = []

        processing_quotes = False
        skip_count = 0

        # Parse each list item and H2.
        # Start getting quotes after the H2 that reads "quotes"
        # Stop parsing after the H2 that reads "quotes about <person>" or "external links"
        for row in soup.find_all(['h2', 'li']):
            if row.name == 'h2':
                # Check for "quotes about" heading to stop processing quotes
                row_text = row.get_text().lower()
                if row_text.startswith('quotes about') or row_text.startswith('external links') or row_text.startswith('misattributed'):
                    break
                # Check for "quotes" heading to start processing quotes
                elif row_text.startswith('quotes') or row_text.startswith('quotations'):
                    processing_quotes = True

            elif processing_quotes and row.name == 'li':
            # how many child elements do we need to skip
                if skip_count > 0:
                    skip_count -= 1
                    continue

                # Get raw quote. Parse the parts of the quote until we find a ul tag.
                # A ul tag is a nested list and we do not want to parse that
                # (it is usually the date, source or context of the quote and not a quote itself)
                quote = row.contents
                if quote is not None:
                    bare_quote = []
                    for part in quote:
                        if part.name == 'ul':
                            skip_count += 1

                        # Can be <a> tag, <br> or <i> in which case we just want the text
                        elif isinstance(part, Tag):
                            bare_quote.append(part.text)

                        # Otherwise it is the text of our li
                        else:
                            bare_quote.append(part)

                    quote = ''.join(bare_quote)

                    if quote.endswith('\n'):
                        quote = quote[:-1]

                    # Filter for numbers ?
                    # if quote is not None and any(char.isdigit() for char in quote):
                    #     quote = None
                # print(quote)
                if quote is not None:
                    quotes.append(quote)
        return quotes
    else:
        print(f"Failed to fetch quotes for {person}")
        return []

def write_quotes_to_files(person, quotes):
    # Shuffle the quotes randomly
    random.shuffle(quotes)

    # Calculate the number of quotes to put in the test set (half of the total quotes)
    num_test_quotes = 1

    # Divide the quotes into train and test sets
    train_quotes = quotes[num_test_quotes:]
    test_quotes = quotes[:num_test_quotes]

    # Write the train quotes to their files in the quotes folder
    folder = 'quotes'
    train_filename = os.path.join(folder, f"{person.replace(' ', '_')}.txt")
    with open(train_filename, 'w') as train_file:
        for quote in train_quotes:
            train_file.write(quote + '\n')

    # Write the test quotes to their files in the test-quotes folder
    test_folder = 'test-quotes'
    test_filename = os.path.join(test_folder, f"{person.replace(' ', '_')}.txt")
    with open(test_filename, 'w') as test_file:
        for quote in test_quotes:
            test_file.write(quote + '\n')

def charlieData():

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
    with open('data/people.txt', 'r') as file:
        people = file.readlines()
        people = [person.strip() for person in people]

    # Crawl wikiquotes page for each person to get their quotes
    for person in people:
        quotes = get_quotes_for_person(person)
        if quotes:
            print(f"Writing quotes for {person} to file...")
            write_quotes_to_files(person, quotes)
            print(f"Quotes for {person} written to {person.replace(' ', '_')}.txt")
            print()
        else:
            print(f"No quotes found for {person}")
            print()
"""