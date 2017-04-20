#!/usr/bin/env python

from strategies import *
from parser import *
from test import *

def main():
    # my_str = 'Tnvnswp {:5 Q., Qmggv I5 VI/ gQ Wlllmvtgllgg Merlmégyi 2 6002; Co1Am0j,0l\"¤€q0rx/ .    Assessor’s Tax Parcel ID Number:   · O 0 ‘   The County Auditor vwll rely on the information provided on    this form. The Staff will not-read the document to verily the `     Accuracy or completeness of the indexing'

    # words = preprocess(my_str)
    # print(words)
    # tokens = create_bag_of_words(words)
    # print(tokens)

    documents = {}

    documents.update(parse_documents_from_directory('../data/DR'))
    documents.update(parse_documents_from_directory('../data/DT'))
    documents.update(parse_documents_from_directory('../data/L'))

    # for document in documents:
    #     print(document, documents[document])

    test_initial_strategies(documents)

if __name__ == '__main__':
    main()
