import requests
from bs4 import BeautifulSoup, Tag
import os
import shutil


def get_quotes_for_person(person):
    base_url = "https://en.wikiquote.org/wiki/"
    person_url = base_url + person.replace(" ", "_")

    response = requests.get(person_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = []

        processing_quotes = False
        skip_count = 0
        for row in soup.find_all(['h2', 'li']):
            if row.name == 'h2':
                # Check for "quotes about" heading to stop processing quotes
                row_text = row.get_text().lower()
                if row_text.startswith('quotes about') or row_text.startswith('external links'):
                    break
                # Check for "quotes" heading to start processing quotes
                elif row_text.startswith('quotes'):
                    processing_quotes = True

            elif processing_quotes and row.name == 'li':
            # how many child elements do we need to skip
                if skip_count > 0:
                    skip_count -= 1
                    continue

                quote = row.contents
                if quote is not None:
                    bare_quote = []
                    for part in quote:
                        if part.name == 'ul':
                            skip_count += 1
                        elif isinstance(part, Tag):
                            bare_quote.append(part.text)
                        else:
                            bare_quote.append(part)

                    quote = ''.join(bare_quote)

                    if quote.endswith('\n'):
                        quote = quote[:-1]

                    # Filter for numbers
                    if quote is not None and any(char.isdigit() for char in quote):
                        quote = None
                # print(quote)
                if quote is not None:
                    quotes.append(quote)

        return quotes
    else:
        print(f"Failed to fetch quotes for {person}")
        return []

def write_quotes_to_file(person, quotes):
    folder = 'quotes'
    filename = os.path.join(folder, f"{person.replace(' ', '_')}.txt")
    with open(filename, 'w') as file:
        for quote in quotes:
            file.write(quote + '\n')

def data():
    # reset data
    folder = 'quotes'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    with open('data/people.txt', 'r') as file:
        people = file.readlines()
        people = [person.strip() for person in people]

    for person in people:
        quotes = get_quotes_for_person(person)
        if quotes:
            print(f"Writing quotes for {person} to file...")
            write_quotes_to_file(person, quotes)
            print(f"Quotes for {person} written to {person.replace(' ', '_')}.txt")
            print()
        else:
            print(f"No quotes found for {person}")
            print()
