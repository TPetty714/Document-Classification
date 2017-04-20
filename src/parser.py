import os
import re


def test_results_match(results):
    """This function takes a dictionary as an argument, which has a file name mapped to its proposed classification. It will open up the test results file and compare it to the dictionary, line by line. It returns a boolean indicating whether or not the classifications match the test results file."""

    test_results = open('../data/test-results.txt', 'r')
    actual = test_results.read()
    actual = actual.split('\n')

    if results == actual:
        test_results.close()
        return True
    else:
        test_results.close()
        return False


def create_bag_of_words(document):
    """This function takes a preprocessed document as an argument and proceeds to create a dictionary, mapping each term to its frequency in the document. It returns a dictionary."""
    document = document.split()

    tokens = {}

    for word in document:
        if word not in tokens:
            tokens[word] = 1
        else:
            tokens[word] += 1

    return tokens


def preprocess(document):
    """This function converts non-alphabetic characters to whitespace, lowercases all letters, and collapses all subsequent whitespace down to a single space. It returns a string of the preprocessed document"""
    document = re.sub(r'\W+', ' ', document)
    document = re.sub(r'\d+', ' ', document)
    document = re.sub(r'\s+', ' ', document)

    document = document.lower()

    return document


def parse_documents_from_directory(direct):
    """This function takes a directory as an argument and traverses each text file in the directory. With each text file, it will preprocess it. It returns a dictionary of all the names of the preprocessed documents mapped to their corresponding text."""
    files = os.listdir(direct)
    preprocessed_documents = {}
    for file in files:
        if file.endswith('.txt'):
            file_d = open("{}/{}".format(direct, file), 'r', encoding='utf8')
            document = file_d.read()
            preprocessed_documents[file] = preprocess(document)
            file_d.close()

    return preprocessed_documents