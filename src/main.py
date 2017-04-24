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
    final_results.write('\n')
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


    argv_iter = iter(sys.argv)
    next(argv_iter)
    for arg in argv_iter:
        print(arg)
        if arg.endswith('DR'):
            normalized_DR = parse_documents_from_directory(arg)
        elif arg.endswith('DT'):
            normalized_DT = parse_documents_from_directory(arg)
        elif arg.endswith('L'):
            normalized_L = parse_documents_from_directory(arg)
        elif arg.endswith('TEST'):
            test_results = parse_documents_from_directory(arg)
        else:
            print('One or more of the directories you provided is not useful for training or testing')
            display_help
            sys.exit()

    # print('{}\n'.format(normalized_DR))
    # print('{}\n'.format(normalized_DT))
    # print('{}\n'.format(normalized_L))

    # expected = classify_with_intelligrep(test_results)
    # test_intelligrep(actual, expected)
    # write_final_results_to_file('I', expected, 'w')

    # training_set = train_tf_idf(normalized_DR, normalized_DT, normalized_L)
    # expected = classify_with_tf_idf(training_set)
    # write_final_results_to_file('T', expected, 'a')


if __name__ == '__main__':
    main()
