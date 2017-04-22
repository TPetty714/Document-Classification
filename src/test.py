from strategies import *


def test_intelligrep(documents):
    print('Now testing intelli-grep...')
    if test_results_match(classify_with_intelligrep(documents)):
        print('Final Status: Success!')
    else:
        print('Final Status: Failure!')


def test_initial_strategies(documents):
    test_intelligrep(documents)


def test_results_match(results):
    """This function takes a dictionary as an argument, which has a file name mapped to a proposed classification. It will open up the actual test results file and break it up into a dictionary. The function will compare the actual test results to the proposed results by inspecting each key and checking to see if the values are identical. It will report each key that fails as well as the number of total failures. It returns a boolean indicating whether or not the classifications match the test results file."""

    test_results_file = open('../data/test-results.txt', 'r')
    test_contents = test_results_file.read()
    test_contents = test_contents.splitlines()

    actual = {}

    for line in test_contents:
        elements = tuple(line.split(','))
        actual[elements[0]] = elements[1]

    results_match = True

    failures = 0
    for key in set(actual) & set(results):
        if actual[key] != results[key]:
            # print('{} did not have a matching classification'.format(key))
            failures += 1
            results_match = False
    print('Failures: {}'.format(failures))

    test_results_file.close()

    return results_match

# just use a dictionary for both intelli grep and the test results
