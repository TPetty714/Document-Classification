#!/usr/bin/env python

import sys

from strategies import *
from parser import *
from test import *


def write_final_results_to_file(strategy, test_results, mode):
    """This function takes three arguments: The name of the strategy, the dictionary mapping the file name to its classification, and the modifier for the open() function. It first opens a file for writing, which will represent the final output file for all the strategies. Then it will iterate through all items in the dictionary, writing each one in succession to the final output file. This function will be called each time a strategy finishes its testing phase and must write its final results out to the file."""
    final_results = open('final_results.txt', mode)
    for key in test_results:
        final_results.write('{}, {}, {}\n'.format(strategy, key, test_results[key]))
    final_results.close()


def display_help():
    print('\nIncorrect usage!\n')
    print('Type \'python3 main.py \'training_dir_1\' \'training_dir_2\' \'training_dir_3\' \'testing_file\'\n')
    print('Where training_dir represents a directory to train the algorithms')
    print('and testing_dir represents a directory with data to test the algorithms\n')


def main():
    if len(sys.argv) != 5:
        display_help()
        sys.exit()

    actual = parse_actual_results('../data/test-results.txt')

    test_results = parse_documents_from_directory(sys.argv[4])
    expected = classify_with_intelligrep(test_results)


    test_intelligrep(actual, expected)
    write_final_results_to_file('I', expected, 'w') # The 'w' creates/overwrites the file you give it, but we may need to review the parameters to modify this function since we want to call this for each initial strategy that is run. We want to create/overwrite the file when we first run it and then append to it as we go
    # From here you can test the remaining strategies


if __name__ == '__main__':
    main()
