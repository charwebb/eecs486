# For EECS 486
# Tweet Prediction

from data.data import data
from model.model import model
from evaluate.evaluate import evaluate

def main():
    # Get Data
    data()

    # Run predictions
    model()

    # Evaluate
    evaluate()

    return

main()
