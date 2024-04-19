# For EECS 486
# TV Character Prediction

from data.data import data
from model.model import model
from evaluate.evaluate import evaluate
import time

def main():
    start = time.time()
    # Get Data
    user_input = input("Do you want to get data? (y/n): ")

    if user_input.lower() == 'y':
        data()

    # Run predictions
    model()

    # Evaluate
    evaluate()
    end = time.time()
    print(f"Execution time: {end - start} seconds")
    return

main()
