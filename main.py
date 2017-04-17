#!/usr/bin/env python

import os
import re

def parse_document(document):
    tokens = []
    # print(document)
    for word in document.split():
        # print(word + '\n')
        word = word.lower()
        word = re.sub(r'\W+', ' ', word)
        word = re.sub(r'\d+', ' ', word)
        word = re.sub(r'\s+', ' ', word)

        tokens.append(word)

    return tokens


def main():
    # parse_document('data/DR/OR_Coos_2008-04-03__08003320.txt')
    my_str = 'Tnvnswp {:5 Q., Qmggv I5 VI/ gQ Wlllmvtgllgg Merlmégyi 2 6002; Co1Am0j,0l\"¤€q0rx/ .    Assessor’s Tax Parcel ID Number:   · O 0 ‘   The County Auditor vwll rely on the information provided on    this form. The Staff will not-read the document to verily the `     Accuracy or completeness of the indexing'
    words = parse_document(my_str)
    print(words)

if __name__ == '__main__':
    main()
