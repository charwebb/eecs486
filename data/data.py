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
    character_counts = df['Character'].value_counts().to_dict()
    character_counts = {k: v for k, v in character_counts.items() if k} # Removes all empties
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35} # Only keeps top occurances
    
    for character in top_character_counts:
            group = df[df['Character'] == character]
            dialogues = group["Dialogue"].tolist()

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
    os.makedirs(output_directory, exist_ok=True)

    df = pd.read_csv(quotes_csv)
    df['Character'] = df['Character'].apply(cleanCharacterColumn)
    df['Line'] = df['Line'].astype(str)
    character_counts = df['Character'].value_counts().to_dict()

    # Removes all empties
    character_counts = {k: v for k, v in character_counts.items() if k}

    # Only keeps top occurances
    top_character_counts = {character: count for character, count in character_counts.items() if count > 35}

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
            # Only keeps top occurances
            if(len(character_quotes[character]) > 35):
                newfile = f"Office_{character.upper()}.txt"
                with open(newfile, 'w') as output:
                    for quote in character_quotes[character]:
                        
                        output.write(quote)
                        output.write("\n")

        return