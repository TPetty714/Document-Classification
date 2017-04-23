#!/usr/bin/env python

import sys

from strategies import *
from parser import *
from test import *


def display_help():
    print('\nIncorrect usage!\n')
    print('Type \'python3 main.py \'training_dir_1\' \'training_dir_2\' \'training_dir_3\' \'testing_file\'\n')
    print('Where training_dir represents a directory to train the algorithms')
    print('and testing_dir represents a directory to test the algorithms\n')


def main():
    if len(sys.argv) != 5:
        display_help()
        sys.exit()

    # d = os.listdir(sys.argv[1])
    # for file in d:
    #     if file.endswith('txt'):
    #         th = open('{}/{}'.format(sys.argv[1], file), 'r')
    #         th.close()
    # d = os.listdir(sys.argv[2])
    # for file in d:
    #     if file.endswith('txt'):
    #         th = open('{}/{}'.format(sys.argv[2], file), 'r')
    #         th.close()
    # d = os.listdir(sys.argv[3])
    # for file in d:
    #     if file.endswith('txt'):
    #         th = open('{}/{}'.format(sys.argv[3], file), 'r')
    #         th.close()
    # file = open(sys.argv[4])
    # file.close()

    # actual = parse_actual_results('../data/test-results.txt')

    # test_results = parse_documents_from_directory('../data/TEST')
    # expected = classify_with_intelligrep(test_results)


    # test_intelligrep(actual, expected)


if __name__ == '__main__':
    main()
