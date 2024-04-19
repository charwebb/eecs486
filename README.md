# Tweet Predictor

Github Repo: https://github.com/charwebb/eecs486

For EECS 486: Information Retrieval

To run this code:

* python3 -m venv env

* source env/bin/activate

* pip3 install -r requirements.txt

* python3 main.py

If you have a stale virtual environment run:

* deactivate

* source env/bin/activate

If you are getting import errors:

* add the needed packages to requirements.txt

and run:

* pip3 install -r requirements.txt

* All required packages must be listed in requirements.txt, not imported ad hoc

## Description ##

This code has 3 main modules to it:

* Data

First, we ask if you want to get fresh data or not. Input 'y' to get data however if you want to bypass and use the previous runs data, input 'n'.

Data takes in nothing but does requrie office_quotes.csv, seinfeld_quotes.csv and southpark_quotes.csv to exist at the root directory. It will parse each of these and create 2 output directories, TVShowQuotes-Train and TVShowQuotes-Test. Right now we have a 90/10 split of training to test data. Each file in these files is named <showname>_<character>.txt respectively.

Note: data/data.py line 14 is where we toggle how many quotes we filter for. Benchmarks for this are provided just above this line and are described in greater detail in our paper.

* Model

Model requires that the TVShowQuotes-Train and TVShowQuotes-Test directories exist and have files in them. It will tokenize all of the data and run VSM 9 times with each of the different weighting shchemes.

Note: See 169-174 for our commented out BERT code. With this uncommented the code may take hours to run however we left it in since it works with very small sample sizes. It is just too computationally stressful to leave in.

Model outputs predictions to the predictions directory. These are named <tokenizing method><weighting scheme>.txt . They are full of dictionaries in the format {character [(character predictions, probability)]}

* Evaluate

Evaluate requires predictions to exist and to contain files with dictionaries of the previosuly stated style in them. It then runs accuracy, macro-averaged precision and recall and the F1 score of each prediction file and outputs this data to the same file, output.txt. This file is of the format:

Prediction Method: <tokenizing method><weighting scheme>
Accuracy:
Macro-averaged Precision:
Macro-averaged Recall:
F1 Macro Score:

For each of the tokenizing methods and weighting schemes.

* main

Main optionally runs data, then model, then evaluate. It requries the csv files to exist and outputs to output.txt. Status updates are printed to the commandline as well as overall execution time at the end.

As benchmarks, with the following characters here are the approximate runtimes:

20 Characters: 42 seconds
100 Characters: 90 seconds
612 Characters: 317 seconds

Note that this is variable depending on what machine you are running on and how long you take to respond to the initial query for data.
