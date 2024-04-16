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

    # Make training and testing directories
    train_dir=output_directory + "-Train"
    test_dir=output_directory + "-Test"
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    df = pd.read_csv(quotes_csv)
    df['Character'] = df['Character'].apply(cleanCharacterColumn)
    df['Dialogue'] = df['Dialogue'].astype(str)
    df = df[df['Dialogue'].apply(lambda x: len(x.split()) > 7)] # Only gets lines with 7+ words

    character_counts = df['Character'].value_counts().to_dict()
    character_counts = {k: v for k, v in character_counts.items() if k} # Removes all empties
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35} # Only keeps top occurances

    for character in top_character_counts:
            group = df[df['Character'] == character]
            dialogues = group["Dialogue"].tolist()
            #print(dialogues)

            random.shuffle(dialogues)
            split_idx = int(len(dialogues) * 0.10)
            test_dialogues = dialogues[:split_idx]
            train_dialogues = dialogues[split_idx:]

            # Filename for each character
            test_filename = os.path.join(test_dir, "Seinfeld_{}.txt".format(character.upper()))
            train_filename = os.path.join(train_dir, "Seinfeld_{}.txt".format(character.upper()))

            with open(test_filename, 'w', encoding='utf-8') as file:
                file.writelines(line + "\n" for line in test_dialogues)

            with open(train_filename, 'w', encoding='utf-8') as file:
                file.writelines(line + "\n" for line in train_dialogues)

    return

def southParkData():
    output_directory = 'TVShowQuotes'
    quotes_csv = 'southpark_quotes.csv'
        # Make training and testing directories
    train_dir=output_directory + "-Train"
    test_dir=output_directory + "-Test"
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    df = pd.read_csv(quotes_csv)
    df['Character'] = df['Character'].apply(cleanCharacterColumn)
    df['Line'] = df['Line'].astype(str)
    df = df[df['Line'].apply(lambda x: len(x.split()) > 7)] # Only gets lines with 7+ words
    character_counts = df['Character'].value_counts().to_dict()

    # Removes all empties
    character_counts = {k: v for k, v in character_counts.items() if k}

    # Only keeps top occurances
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35}

    for character in top_character_counts:
        group = df[df['Character'] == character]
        lines = group["Line"].tolist()
        random.shuffle(lines)

        split_idx = int(len(lines) * 0.10)
        test_lines = lines[:split_idx]
        train_lines = lines[split_idx:]

        # Filename for each character
        test_filename = os.path.join(test_dir, "SouthPark_{}.txt".format(character.upper()))
        train_filename = os.path.join(train_dir, "SouthPark_{}.txt".format(character.upper()))

        with open(test_filename, 'w', encoding='utf-8') as file:
            file.writelines(line + "\n" for line in test_lines)

        with open(train_filename, 'w', encoding='utf-8') as file:
            file.writelines(line + "\n" for line in train_lines)
    return

def officeData():
    quotes_csv = 'office_quotes.csv'
    output_directory = 'TVShowQuotes'

    # Make training and testing directories
    train_dir=output_directory + "-Train"
    test_dir=output_directory + "-Test"
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    character_quotes = {}

    with open(quotes_csv, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            character = row['speaker']
            script = row['line_text']

            if len(script.split()) > 7:
                charList = character.split("/")
                for char in charList:
                    if char in character_quotes:
                        character_quotes[char].append(script)
                    else:
                        character_quotes[char] = [script]

        for character in character_quotes:
            quotes = character_quotes[character]
            # Only keeps top occurances
            if(len(quotes) > 35):
                random.shuffle(quotes)
                split_idx = int(len(quotes) * 0.10)
                test_quotes = quotes[:split_idx]
                train_quotes = quotes[split_idx:]
                # Filename for each character
                test_filename = os.path.join(test_dir, "TheOffice_{}.txt".format(character.upper()))
                train_filename = os.path.join(train_dir, "TheOffice_{}.txt".format(character.upper()))

                with open(test_filename, 'w', encoding='utf-8') as file:
                    file.writelines(line + "\n" for line in test_quotes)

                with open(train_filename, 'w', encoding='utf-8') as file:
                    file.writelines(line + "\n" for line in train_quotes)


        return
