#!/usr/bin/env python

import os
import re

import strategies

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

    return preprocessed_documents

def main():
    # my_str = 'Tnvnswp {:5 Q., Qmggv I5 VI/ gQ Wlllmvtgllgg Merlmégyi 2 6002; Co1Am0j,0l\"¤€q0rx/ .    Assessor’s Tax Parcel ID Number:   · O 0 ‘   The County Auditor vwll rely on the information provided on    this form. The Staff will not-read the document to verily the `     Accuracy or completeness of the indexing'

    # words = preprocess(my_str)
    # print(words)
    # tokens = create_bag_of_words(words)
    # print(tokens)

    documents = {}

    documents.update(parse_documents_from_directory('data/DR'))
    documents.update(parse_documents_from_directory('data/DT'))
    documents.update(parse_documents_from_directory('data/L'))

    for document in documents:
        print(document, documents[document])

    # print(words)
    print("Success!")

if __name__ == '__main__':
    main()
