import operator
import sys
from math import log10


def determine_classification(DR_weight, DT_weight, L_weight):
    """This function takes three floats as arguments, representing weights from each of the three classification categories. The function determines the classification with the largest weight and returns it as an entry for a dictionary."""
    if DR_weight > DT_weight and DR_weight > L_weight:
        classification = 'DT'
    elif DT_weight > DR_weight and DT_weight > L_weight:
        classification = 'DR'
    elif L_weight > DT_weight and L_weight > DR_weight:
        classification = 'L'
    elif DR_weight == DT_weight or DR_weight == L_weight:
        classification = 'DT'
    elif DT_weight == L_weight:
        classification = 'DR'
    else:
        classification = 'DR'

    return classification


def classify_with_intelligrep(documents):
    """This function takes a dictionary as an argument representing the name of preprocessed documents mapped to their corresponding content. Intelli-grep traverses each one and looks for patterns in the strings in order to classify it. The specific string pattern that occurs the most often in the document is how this function will classify it. If there is a tie between word frequencies, a classification will be made in this order of precedence: DR, DT, L. It returns a dictionary that maps each document name with its corresponding classification"""
    results = {}

    for document in documents:
        deed_of_trust_count = documents[document].count('deed of trust')
        deed_of_reconveyance_count = documents[document].count('deed of reconveyance')
        lien_count = documents[document].count('lien')

        results[document] = determine_classification(float(deed_of_trust_count), float(deed_of_reconveyance_count), float(lien_count))

    return results


def classify_with_tf_idf(DR_dict, DT_dict, L_dict, test_documents):
    """This function takes a three dictionaries as arguments representing the word vectors for the DR, DT, and L categories. It will create a new list for each category containing words that occur more in that category in comparison to the other categories. Simply put, there is no intersection between the lists it creates. The function will iterate through all the documents in the TEST directory and will use the lists in order to help determine to which category each document belongs. It returns a dictionary mapping the name of each file to its proposed classification."""
    classifications = {}

    DR_weight = 0.0
    DT_weight = 0.0
    L_weight = 0.0

    for document in test_documents:
        for word in document.split():
            best_classifier = '?'

            if word in DR_dict:
                best_classifier = 'DR'
                if word in DT_dict and DT_dict[word] > DR_dict[word]:
                    best_classifier = 'DT'
                if word in L_dict and L_dict[word] > DR_dict[word]:
                    best_classifier = 'L'
            elif word in DT_dict:
                best_classifier = 'DT'
                if word in DR_dict and DR_dict[word] > DT_dict[word]:
                    best_classifier = 'DR'
                if word in L_dict and L_dict[word] > DT_dict[word]:
                    best_classifier = 'L'
            elif word in L_dict:
                best_classifier = 'L'
                if word in DR_dict and DR_dict[word] > L_dict[word]:
                    best_classifier = 'DR'
                if word in DT_dict and DT_dict[word] > L_dict[word]:
                    best_classifier = 'DT'

            if best_classifier == 'DR':
                DR_weight += DR_dict[word]
            if best_classifier == 'DT':
                DT_weight += DT_dict[word]
            if best_classifier == 'L':
                L_weight += L_dict[word]

        classifications[document] = determine_classification(DR_weight, DT_weight, L_weight)


    return classifications


def create_ratioed_word_frequency_dict_list(training_dir):
    """This function takes a dictionary with a file name mapped to its preprocessed text. The function should be passed a set of documents where the classifier is already known. It traverses each body of text and creates a dictionary mapping each term with its frequency in the document. It then iterates through each term in the dictionary and converts the frequency into a ratio by dividing its frequency by the total number of words in the document. It will return a dictionary that includes each word mapped to its respective ratioed word frequency."""
    dict_list = []
    for document in training_dir:
        curr_document = training_dir[document].split()
        terms = {}
        for word in curr_document:
            if word not in terms:
                terms[word] = 1.0
            else:
                terms[word] += 1.0
        total_words_in_document = len(curr_document)
        for term in terms:
            terms[term] = float(terms[term] / total_words_in_document)
        dict_list.append(terms)

    return dict_list


def create_normalized_ratioed_word_frequency_dict(word_list_to_be_ratioed, word_list1, word_list2):
    new_ratioed_dict = {}
    for word_bag in word_list_to_be_ratioed:
        for word in word_bag:
            if word in new_ratioed_dict:
                new_ratioed_dict[word] += word_bag[word]
            else:
                new_ratioed_dict[word] = 1

    total_documents = len(word_list_to_be_ratioed) + len(word_list1) + len(word_list2)

    for word in new_ratioed_dict:
        num_documents_with_word = 0
        for word_bag in word_list_to_be_ratioed:
            if word in word_bag:
                num_documents_with_word += 1
        for word_bag in word_list1:
            if word in word_bag:
                num_documents_with_word += 1
        for word_bag in word_list2:
            if word in word_bag:
                num_documents_with_word += 1
        weight = log10(total_documents / num_documents_with_word)
        new_ratioed_dict[word] *= weight
        # print('Documents with {}: {}'.format(word, num_documents_with_word))


    return new_ratioed_dict


def train_tf_idf(normalized_DR, normalized_DT, normalized_L, test_results):
    """This function trains the TF-IDF strategy by feeding it the training directories. This function creates a dictionary for each training set. It first finds the frequency of each word in each dictionary and weighs it by dividing the word frequency by the number of words in each document. Then each dictionary is tested against the other dictionaries by searching to see the number of documents in the other categories that contain each word at least once. The total number of documents is divided by each quantity, and the logarithmic value of this quotient is used as a multiplier to weigh the current frequency even further. Each dictionary with its weighted frequencies is returned as a tuple."""
    relative_DR_frequencies_list = create_ratioed_word_frequency_dict_list(normalized_DR)
    relative_DT_frequencies_list = create_ratioed_word_frequency_dict_list(normalized_DT)
    relative_L_frequencies_list = create_ratioed_word_frequency_dict_list(normalized_L)


    normalized_relative_DR_frequencies = create_normalized_ratioed_word_frequency_dict(relative_DR_frequencies_list, relative_DT_frequencies_list, relative_L_frequencies_list)
    normalized_relative_DT_frequencies = create_normalized_ratioed_word_frequency_dict(relative_DT_frequencies_list, relative_DR_frequencies_list, relative_L_frequencies_list)
    normalized_relative_L_frequencies = create_normalized_ratioed_word_frequency_dict(relative_L_frequencies_list, relative_DR_frequencies_list, relative_DT_frequencies_list)

    # print('{}\n'.format(normalized_relative_DR_frequencies))
    # print('{}\n'.format(normalized_relative_DT_frequencies))
    # print('{}\n'.format(normalized_relative_L_frequencies))


    return classify_with_tf_idf(normalized_relative_DR_frequencies, normalized_relative_DT_frequencies, normalized_relative_L_frequencies, test_results)

