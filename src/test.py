import os

from strategies import *


def test_intelligrep(documents):
    print('Now testing intelli-grep...')
    if test_results_match(classify_with_intelligrep(documents)):
        print('Success!')
    else:
        print('Failure!')


def test_initial_strategies(documents):
    test_intelligrep(documents)


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