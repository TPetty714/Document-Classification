import operator
import sys
from math import log10
import random
import pickle
from parser import *


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

class perceptron:
    def wordBag(documents):
        wordBags = {}

        documentWordCount = {}
        contents = {}
        for document in documents:
            documentWordCount[document] = 0
            # print('++++++++++++' + document + '++++++++++++')s
            wordBag = {}
            for word in documents[document].split():
                documentWordCount[document] += 1
                if word in wordBag.keys():
                    wordBag[word] += 1
                else:
                    wordBag[word] = 1
            for word in wordBag.keys():
                # print(word)
                # print('wordBag: ', wordBag[word])
                wordBag[word] = wordBag[word]/documentWordCount[document]
                wordBags[document] = wordBag
                # print('wordBag/totalcount: ', wordBag[word])
                # print(word + ': ' + str(wordBag[word])            wordBags[document] = wordBag
        return wordBags

    def featureSet(documents):
        wordList = {}
        totalWordCount = 0
        feature = {}
        featureSet = list()
        for document in documents:
            for word in documents[document].split():
                totalWordCount += 1
                if word in wordList.keys():
                    wordList[word] += 1
                else:
                    wordList[word] = 1
                # print(word + ':' + str(wordBag[word]))
        for words in wordList:
            featureSet.append((wordList[words], words))
        # Sorts featureSet and takes top 20 words
        featureSet.sort(reverse=True)
        for i in range (20):
            feature[featureSet[i][1]] = featureSet[i][0]/totalWordCount
            # print(str(featureSet[i]))
        # # print('Total Word Count = ',str(totalWordCount))
        # return feature
        return feature

    def setCombiner(DR, DT, L):
        feature = {}
        filesFromSets = 40
        DRL = list(DR.keys())
        DTL = list(DT.keys())
        LL = list(L.keys())

        random.shuffle(DRL)
        random.shuffle(DTL)
        random.shuffle(LL)

        for i in range(len(DRL)):
            # print(DR[word])
            feature[DRL[i]] = DR[DRL[i]]
        for i in range(len(DTL)):
            # print(DT[word])
            feature[DTL[i]] = DT[DTL[i]]
        for i in range(len(LL)):
            # print(L[word])
            feature[LL[i]] = L[LL[i]]
        return feature

    def Combiner(DR,DT,L):
        feature = {}
        DRL = DR.keys()
        DTL = DT.keys()
        LL = L.keys()

        for word in DR.keys():
            # print(DR[word])
            feature[word] = DR[word]
        for word in DT.keys():
            # print(DT[word])
            feature[word] = DT[word]
        for word in L.keys():
            # print(L[word])
            feature[word] = L[word]
        return feature


    def Combiner(DR,DT,L):
        feature = {}
        for word in DR.keys():
            # print(DR[word])
            feature[word] = DR[word]
        for word in DT.keys():
            # print(DT[word])
            feature[word] = DT[word]
        for word in L.keys():
            # print(L[word])
            feature[word] = L[word]
        return feature

    def printWeights(weight):
        for document in weight.keys():
            print(document + " weights: " + str(weight[document]))

    def learning(documents, wordBags, featureSet, answers, expected, weight = {}, Bias = -0.5):
        alpha = 0.11
        globalError = 1
        voteNum = {}
        if weight == {}:
            for word in featureSet.keys():
                weight[word] = random.uniform(-1,1)
        # print("Documents set size: " + str(len(documents)))
        for i in range (100):
            # print('Iteration number = ' + str(i))

            # if globalError == 0:
            #     pickle.dump(weight, open('../data/weights' + expected + '.p', 'wb'))
            #     pickle.dump(Bias, open('../data/bias' + expected + '.p', 'wb'))
            #     pickle.dump(alpha, open('../data/alpha' + expected + '.p', 'wb'))
            #     return weight
            # globalError = 0
            alpha *= 0.99

            docList = list(documents.keys())
            dictCount = 0
            random.shuffle(docList)
            # print("Documents set size: " + str(len(documents)))
            # print("DocList set size: " + str(len(docList)))
            for document in docList:

                # print("Documents set size: " + str(len(documents)))
                dictCount += 1
                # docList.remove(document)
                # print(str(dictCount) + ': ' + document)
                err = 1
                while err != 0:
                    Pc = 0
                    # print('Word Count: ' + str(len(featureSet)) )
                    for word in weight.keys():
                        # sum from 0 to n (Wj*xj[e])
                        if word in wordBags[document]:
                            try:
                                Pc += weight[word]*wordBags[document][word]
                            except KeyError:
                                print(word + ' not in lists')
                    Pc += Bias
                    # print('Iteration number = ' + str(i))
                    # print('alpha: ' + str(alpha))
                    # print('Learning Pc: ' + str(Pc))
                    if Pc <= 0:
                        voteNum[document] = 0
                    else:
                        voteNum[document] = 1
                    # print('Learning vote: ' + str(voteNum[document]))
                    if document in answers:
                        err = 1 - voteNum[document]
                        print('Vote err: ' + str(err) + ' = 1 - ' + str(voteNum[document]))
                    else:
                        err = 0 - voteNum[document]
                        print('Vote err: ' + str(err) + ' = 0 - ' + str(voteNum[document]))
                    if err != 0:
                        for word in weight.keys():
                            if word in wordBags[document]:
                                try:
                                    weight[word] = weight[word] + alpha*err*wordBags[document][word]
                                except KeyError:
                                    print(word + ' not in weights')
                    # print('Bias: ' + str(Bias) + 'alpha: ' + str(alpha) + 'err: ' + str(err))
                    Bias = Bias + alpha*err
                # print('Weight: ', end = ' ')
                # for wght in weight:
                     # print(str(weight[wght]), end = ' ')
                # print('\nBias: ' + str(Bias))
        pickle.dump(weight, open('../data/weights' + expected + '.p', 'wb'))
        pickle.dump(Bias, open('../data/bias' + expected + '.p', 'wb'))
        # return (weight, Bias)

    def testing(documents, wordBags, featureSet, answers, expected, weight = {}, Bias = -0.5):

        success = 0
        total = 0
        voteNum = {}
        # print("Documents set size: " + str(len(documents)))

        docList = list(documents.keys())
        random.shuffle(docList)
        # print("Documents set size: " + str(len(documents)))
        # print("DocList set size: " + str(len(docList)))
        for document in docList:
            # print(document)
            Pc = 0
            total += 1
            # print("Documents set size: " + str(len(documents)))
            # dictCount += 1
            # docList.remove(document)
            # print(str(dictCount) + ': ' + document)
                # print('Word Count: ' + str(len(featureSet)) )
            for word in weight.keys():
                # sum from 0 to n (Wj*xj[e])
                if word in wordBags[document]:
                    try:
                        Pc += weight[word]*wordBags[document][word]
                        # print('Word weight: ' + str(weight[word]) + ' WordBag: ' + str(wordBags[document][word]))
                    except KeyError:
                        print(word + ' not in lists')
            Pc += Bias
            # print('Pc: ' + str(Pc))
            if Pc <= 0:
                vote = 'other'
                voteNum[document] = 0
            else:
                vote = expected
                voteNum[document] = 1
            # print(expected + " vote " + str(voteNum[document]))
        return voteNum

    def voteTally(DRVotes, DTVotes, LVotes, test, actual):
        total = 0
        success = 0
        votes = {}
        for document in test:
            # print(str(DRVotes[document]))
            # print(str(DRVotes[document]))
            # print(str(DRVotes[document]))
            tieBreaker = 0
            total += 1
            # print(actual[document])
            if DRVotes[document] == DTVotes[document]:
                tieBreaker = random.uniform(0, 1)
                if tieBreaker == 0:
                    DRVotes[document] = 1
                    DTVotes[document] = 0
                    votes[document] = 'DR'
                else:
                    DRVotes[document] = 0
                    DTVotes[document] = 1
                    votes[document] = 'DT'
            if DRVotes == LVotes:
                tieBreaker = random.uniform(0, 1)
                if tieBreaker == 0:
                    DRVotes[document] = 1
                    LVotes[document] = 0
                    votes[document] = 'DR'
                else:
                    DRVotes[document] = 0
                    LVotes[document] = 1
                    votes[document] = 'L'
            if DTVotes[document] == LVotes[document]:
                tieBreaker = random.uniform(0, 1)
                if tieBreaker == 0:
                    DTVotes[document] = 1
                    LVotes[document] = 0
                    votes[document] = 'DT'
                else:
                    DTVotes[document] = 0
                    LVotes[document] = 1
                    votes[document] = 'L'
            if DRVotes[document] == DTVotes[document] == LVotes[document]:
                tieBreaker = random.uniform(0,2)
                if tieBreaker == 0:
                    DRVotes[document] = 1
                    DTVotes[document] = 0
                    LVotes[document] = 0
                    votes[document] = 'DR'
                if tieBreaker == 0:
                    DRVotes[document] = 0
                    DTVotes[document] = 1
                    LVotes[document] = 0
                    votes[document] = 'DT'
                if tieBreaker == 0:
                    DRVotes[document] = 0
                    DTVotes[document] = 0
                    LVotes[document] = 1
                    votes[document] = 'L'
            if actual[document] == 'DR':
                if DRVotes[document] == 1 and DTVotes[document] == 0 and LVotes[document] == 0:
                    success += 1
            if actual[document] == 'DT':
                if DRVotes[document] == 0 and DTVotes[document] == 1 and LVotes[document] == 0:
                    success += 1
            if actual[document] == 'L':
                if DRVotes[document] == 0 and DTVotes[document] == 0 and LVotes[document] == 1:
                    success += 1
        # print('Result: ' + str(success/total))
        return votes