# For EECS 486
# Tweet Prediction

from data.data import data
from model.model import model
from evaluate.evaluate import evaluate

def main():
    # Get Data
    user_input = input("Do you want to get data? (y/n): ")

    if user_input.lower() == 'y':
        data()

    # Run predictions
    model()

    # Evaluate
    evaluate()

    return

main()
