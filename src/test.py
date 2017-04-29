from strategies import *


def test_strategy(strategy, actual, expected):
    """This function takes the name of a strategy as well as two dictionaries as arguments: 'actual' representing the dictionary actually parsed from the test file, and 'expected' representing the dictionary proposed by intelligrep. Both dictionaries contain keys representing the file names mapped to their classification. The function will iterate through each shared key in the dictionaries and verify whether the classifications match. It outputs the number of failures in addition to an option to print each failing key. Finally, it outputs whether the test failed or not. It returns void."""
    num_documents = len(actual)
    print('\nNow testing {}...'.format(strategy))

    correct_answers = 0
    for key in set(actual) & set(expected):
        if actual[key] == expected[key]:
            correct_answers += 1
    accuracy = (correct_answers / num_documents) * 100
    print('Accuracy: {}'.format(accuracy))
