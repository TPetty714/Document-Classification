#!/usr/bin/env python

import os
import re

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

def preprocess_document(document):
    """This function converts non-alphabetic characters to whitespace, lowercases all letters, and collapses all subsequent whitespace down to a single space. It returns a string of the preprocessed document"""
    document = re.sub(r'\W+', ' ', document)
    document = re.sub(r'\d+', ' ', document)
    document = re.sub(r'\s+', ' ', document)

    document = document.lower()

    return document

def parse_documents(direct):
    """This function takes a directory as an argument and traverses each text file in the directory. With each text file, it will preprocess it. It returns void."""
    files = os.listdir(direct)
    for file in files:
        if file.endswith('.txt'):
            file_d = open("{}/{}".format(direct, file), 'r', encoding='utf8')
            document = file_d.read()
            words = preprocess_document(document)

def main():
    my_str = 'Tnvnswp {:5 Q., Qmggv I5 VI/ gQ Wlllmvtgllgg Merlmégyi 2 6002; Co1Am0j,0l\"¤€q0rx/ .    Assessor’s Tax Parcel ID Number:   · O 0 ‘   The County Auditor vwll rely on the information provided on    this form. The Staff will not-read the document to verily the `     Accuracy or completeness of the indexing'

    words = preprocess_document(my_str)
    print(words)
    tokens = create_bag_of_words(words)
    print(tokens)

    # parse_documents('data/DR')
    # parse_documents('data/DT')
    # parse_documents('data/L')

    # print(words)
    print("Success!")

if __name__ == '__main__':
    main()
