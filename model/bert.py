import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

# Load data
def bert(training_quotes_dictionary, test_quotes_dictionary):

    # flatten data so it is of type dataFrame like:
    # quote        author
    # "something"  office_jim
    # "else"       southpark_kenny
    # ... etc.

    print("flattening data into data frames")

    flattened_training_data = [(quote, author) for author, quotes in training_quotes_dictionary.items() for quote in quotes]
    flattened_test_data = [(quote, author) for author, quotes in test_quotes_dictionary.items() for quote in quotes]
    train_df = pd.DataFrame(flattened_training_data, columns=['quote', 'character'])
    val_df = train_df.sample(frac=0.1, random_state=12)
    train_df = train_df.drop(val_df.index)
    test_df = pd.DataFrame(flattened_test_data, columns=['quote', 'character'])

    # print(train_df)
    # print(val_df)
    # print(test_df)

    print("tokenizing data")

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    X_train = tokenizer(train_df['quote'].tolist(), padding=True, truncation=True, max_length=256, return_tensors='tf')
    X_val = tokenizer(val_df['quote'].tolist(), padding=True, truncation=True, max_length=256, return_tensors='tf')
    X_test = tokenizer(test_df['quote'].tolist(), padding=True, truncation=True, max_length=256, return_tensors='tf')

    X_train = {key: X_train[key].numpy() for key in X_train}
    X_val = {key: X_val[key].numpy() for key in X_val}
    X_test = {key: X_test[key].numpy() for key in X_test}

    # print(X_train)
    # print(X_val)
    # print(X_test)

    # Encode labels

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(train_df['character'])
    y_val = label_encoder.transform(val_df['character'])
    num_classes = len(label_encoder.classes_)
    print(num_classes)

    # print(y_train)
    # print(y_val)

    model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_classes)

    optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=2e-5)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    metrics = [tf.keras.metrics.SparseCategoricalAccuracy('accuracy')]
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=2,
    batch_size=32
    )

    test_loss, test_acc = model.evaluate(X_val, y_val)
    print(f'Validation accuracy: {test_acc}')

    predictions = model.predict(X_test)
    predicted_labels = np.argmax(predictions.logits, axis=1)

    predicted_labels_original = label_encoder.inverse_transform(predicted_labels)

    # print(X_test)
    # print(predicted_labels_original)

    # Initialize dictionary to store actual test labels and predicted labels with percentages
    predicted_labels_dict = {}

    # Loop through each actual test label and corresponding predicted label
    for actual_label, predicted_label in zip(test_df['character'], predicted_labels_original):
        # If the actual label is not already in the dictionary, add it with an empty list as value
        if actual_label not in predicted_labels_dict:
            predicted_labels_dict[actual_label] = []

        # Append the predicted label to the list of corresponding predicted labels
        predicted_labels_dict[actual_label].append(predicted_label)

    # Calculate the percentage of predictions for each actual test label
    for actual_label, predicted_labels in predicted_labels_dict.items():
        # Count the occurrences of each predicted label
        label_counts = pd.Series(predicted_labels).value_counts()

        # Calculate the percentage of predictions for each predicted label
        percentages = [(label, count / len(predicted_labels)) for label, count in label_counts.items()]

        # Update the dictionary with predicted labels and their percentages
        predicted_labels_dict[actual_label] = percentages

    return predicted_labels_dict
