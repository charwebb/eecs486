import os

def precision(character, queriedDocuments):
    retrieved_documents = set([docid for docid, _ in queriedDocuments.get(character, [])])
    relevantDocument = set([character])

    if len(retrieved_documents) == 0:
        return 0

    truePositives = len(retrieved_documents.intersection(relevantDocument))
    return truePositives / len(retrieved_documents)

def recall(character, queriedDocuments):
    retrieved_documents = set([docid for docid, _ in queriedDocuments.get(character, [])])
    relevantDocument = set([character])

    if len(relevantDocument) == 0:
        return 0

    truePositives = len(retrieved_documents.intersection(relevantDocument))

    return truePositives / len(relevantDocument)

def macro_averaged_precision_recall(queriedDocuments):
    totalPrecision = 0
    totalRecall = 0
    numQueries = len(queriedDocuments)

    for character in queriedDocuments.keys():
        totalPrecision += precision(character, queriedDocuments)
        totalRecall += recall(character, queriedDocuments)

    macroPrecision = totalPrecision / numQueries
    macroRecall = totalRecall / numQueries

    return macroPrecision, macroRecall

def calculate_accuracy(queriedDocuments):
    correct_count = 0
    total_count = 0

    for correct, retrieved_docs in queriedDocuments.items():
        # Check if there are any retrieved documents for the queryid
        if retrieved_docs:
            # Get the top-ranked document for the queryid
            top_ranked_document = retrieved_docs[0][0]

            # Check if the top-ranked document matches the correct document
            if top_ranked_document == correct:
                correct_count += 1

            total_count += 1

    # Calculate accuracy
    if total_count > 0:
        accuracy = correct_count / total_count
    else:
        accuracy = 0.0

    return accuracy

def read_predictions_from_file(file_path):
    predictions = {}
    with open(file_path, 'r') as file:
        string_predictions = file.readline()
        predictions = eval(string_predictions)
    return predictions

def evaluate():
    print()
    print("--- evaluating predictions ---")

    predictions_directory = "predictions"
    output_file = "output.txt"
    # Dictionary to store results organized by prediction method
    results_by_method = {}

    # Iterate over prediction files in the predictions directory
    for filename in os.listdir(predictions_directory):
        method_name = filename.split('.')[0]  # Extract prediction method name
        file_path = os.path.join(predictions_directory, filename)

        # Read predictions from the file
        predictions = read_predictions_from_file(file_path)

        macroPrecision, macroRecall = macro_averaged_precision_recall(predictions)
        accuracy = calculate_accuracy(predictions)

        f1_macro = 2 * (macroPrecision * macroRecall) / (macroPrecision + macroRecall)

        # Store results by prediction method
        results_by_method[method_name] = {
            'Accuracy': accuracy,
            'Macro-averaged Precision': macroPrecision,
            'Macro-averaged Recall': macroRecall,
            'F1 Macro Score': f1_macro,
        }

    # Write results to output file
    with open(output_file, 'w') as outfile:
        for method_name, results in sorted(results_by_method.items()):
            outfile.write(f"Prediction Method: {method_name}\n")
            for metric, value in results.items():
                outfile.write(f"{metric}: {value:.4f}\n")
            outfile.write("\n")
