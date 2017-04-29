import os
import re

def preprocess(document):
    """This function converts non-alphabetic characters to whitespace, lowercases all letters, and collapses all subsequent whitespace down to a single space. It returns a string of the preprocessed document"""
    document = re.sub(r'\W+', ' ', document)
    document = re.sub(r'\d+', ' ', document)
    document = re.sub(r'\s+', ' ', document)

    document = document.lower()

    return document


def parse_documents_from_directory(direct):
    """This function takes a directory as an argument and traverses each text file in the directory. With each text file, it will preprocess it. It returns a dictionary of all the names of the preprocessed documents mapped to their corresponding preprocessed text. The dictionary that is returned can then be used to implement an initial strategy."""
    files = os.listdir(direct)
    preprocessed_documents = {}
    for file in files:
        if file.endswith('.txt'):
            file_d = open("{}/{}".format(direct, file), 'r', encoding='utf8')
            document = file_d.read()
            preprocessed_documents[file] = preprocess(document)
            file_d.close()

    return preprocessed_documents


def parse_actual_results(actual_test_results):
    test_results_file = open(actual_test_results, 'r')
    test_contents = test_results_file.read()
    test_contents = test_contents.splitlines()

    actual = {}

    for line in test_contents:
        elements = tuple(line.split(','))
        actual[elements[0]] = elements[1]

    test_results_file.close()

    return actual
