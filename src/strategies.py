import operator


def classify_with_intelligrep(documents):
    """This function takes a dictionary as an argument representing the name of preprocessed documents mapped to their corresponding content. Intelli-grep traverses each one and looks for patterns in the strings in order to classify it. The specific string pattern that occurs the most often in the document is how this function will classify it. It returns a formatted list of strings that includes each document name with its classification"""
    results = []

    for document in documents:

        deed_of_trust_count = documents[document].count('deed of trust')
        deed_of_reconveyance_count = documents[document].count('deed of reconveyance')
        lien_count = documents[document].count('lien')

        if deed_of_trust_count > deed_of_reconveyance_count and deed_of_trust_count > lien_count:
            classification = 'DT'
        elif deed_of_reconveyance_count > deed_of_trust_count and deed_of_reconveyance_count > lien_count:
            classification = 'DR'
        elif lien_count > deed_of_reconveyance_count and lien_count > deed_of_trust_count:
            classification = 'L'
        else:
            print('Intelli-grep was unable to determine a classification for {}'.format(document))
            classification = '?'

        results.append(document + ',' + classification)

    return results

