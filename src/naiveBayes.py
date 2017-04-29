from math import *
def train_naive(DR, DT, L, TEST):#might include test file
	##create stop words to be removed
	stopword_list = generate_stopwords()
	##create the feature set of the training files
	training_feature_set = training_feature_sets(DR, DT, L, stopword_list)
	#print(training_feature_set)
	##find the probablities of training documents
	DR_probablity = training_probablity(training_feature_set, DR)	##P( w|c ) features in documents given class
	DT_probablity = training_probablity(training_feature_set, DT) ##P( w|c ) features in documents given class
	L_probablity = training_probablity(training_feature_set, L) ##P( w|c ) features in documents given class
	
	#start testing
	test_bool = {}
	for name in TEST:
		test_bool[name] = create_bool_bag(training_feature_set, TEST[name])
	#print(test_bag)
	check = naive(test_bool, training_feature_set, DR_probablity, DT_probablity, L_probablity, len(DR), len(DT), len(L), len(TEST))
	print(check)

def naive(test_bag, features,  DR_prob, DT_prob, L_prob, DR, DT, L, TEST):
	##do naive bayes?
	DR_log = log((DR/(DR+DT+L)))
	DT_log = log((DT/(DR+DT+L)))
	L_log = log((L/(DR+DT+L)))
	test_prob = {}
	for x in test_bag:
		test_prob[x] = probablity(features, test_bag[x])
	#run through first document
	prob_sum = {}
	dr_prob = 0
	dt_prob = 0
	l_prob = 0
	for x in DR_prob:
		dr_prob += DR_prob[x]
	for x in DT_prob:
		dt_prob += DT_prob[x]
	for x in L_prob:
		l_prob += L_prob[x]
		
	for x in test_prob:
		total=0
		for y in test_prob[x]:
			total+=test_prob[x][y]
		
		
		dr = DR_log*log((total/dr_prob))
		dt = DT_log*log((total/dt_prob))
		l = L_log*log((total/l_prob))
		
		if dr > dt and dr > l:
			prob_sum[x] = 'DR'
		elif dt > dr and dt > l:
			prob_sum[x] = 'DT'
		elif l > dr and l > dt:
			prob_sum[x] = 'L'
	
	return prob_sum
	
	
def training_create_feature_set(DR_word_bag, DT_word_bag, L_word_bag): ##should be done
	##top 20 words that show up in the class bag of words
	feature_list = {}
	
	DR_features = create_features(DR_word_bag)
	DT_features = create_features(DT_word_bag)
	L_features = create_features(L_word_bag)
	
	for x in DT_features:
		if x not in DR_features:
			DR_features[x] = DT_features[x]
	for x in L_features:
		if x not in DR_features:
			DR_features[x] = L_features[x]
	
	return DR_features

def create_features(word_bag): ##should be done
	feature_list = {}
	temp_list = []
	for x in word_bag:
		temp_list.append((word_bag[x], x))
	temp_list.sort(reverse=True)
	temp_list = temp_list[:20]
	for x, y in temp_list:
		feature_list[y]=x
	return feature_list

def generate_stopwords():
	word_file=open('stopwords.txt', 'r')
	word_list= []
	for line in word_file:
		word_list.append(line.strip('\n'))
	##print(word_list)
	return word_list
	
def probablity(features, document):
	total_word_prob = {}
	for x in document:
		if x not in total_word_prob.keys():
			total_word_prob[x] = document[x]
		else:
			total_word_prob[x] += document[x]
	for x in total_word_prob:
		if total_word_prob[x] == 0:
			total_word_prob[x] = 1/len(document)
		else:
			total_word_prob[x] = total_word_prob[x]/len(document)
	##total probably of words in document
	return total_word_prob
	
def training_probablity(features, document):
	##create a boolean bag for the words in the document
	bool_bag = create_bool_bag(features, document)
	total_word_prob = {}
	for x in bool_bag:
		for y in bool_bag[x]:
			if y not in total_word_prob.keys():
				total_word_prob[y] = bool_bag[x][y]
			else:
				total_word_prob[y] += bool_bag[x][y]
	#print(total_word_prob)
	
	for x in total_word_prob:
		if total_word_prob[x] == 0:
			total_word_prob[x] = 1/len(document)
		else:
			total_word_prob[x] = total_word_prob[x]/len(document)
	##total probably of words in document
	return total_word_prob
	
def create_bag_of_words(document, stopwords): ##method is which function has called this method
	##takes in a dictionary formated as {'filename':'words in dictionary'}
	total_word_count = 0
	doc_words_without_stopwords = []
	#if mode == 1:
		
	for name in document:
		if type(document) is dict:
			word_list = document[name].split()
		else:
			word_list = document.split()
		for word in word_list:
			if word not in stopwords:
				doc_words_without_stopwords.append(word)
				total_word_count+=1
	wordz = {} 
	for word in doc_words_without_stopwords:
		if word not in wordz:
			wordz[word]=1
		else:
			wordz[word]+=1
	for word in wordz:
		wordz[word] = wordz[word]/total_word_count
		
	return wordz ##return dictionary of {'word':'count'}

def training_feature_sets(DR, DT, L, stopwords):	##this should be done with STOP TOUCHING
	
	DR_word_bag = create_bag_of_words(DR, stopwords)
	DT_word_bag = create_bag_of_words(DT, stopwords)
	L_word_bag = create_bag_of_words(L, stopwords)
	
	feature_set=training_create_feature_set(DR_word_bag, DT_word_bag, L_word_bag)
	
	return feature_set

def create_bool_bag(features, document):#, stoplist): not sure spotlist is needed
	##end up returning a dictionary organized as such {document name: {feature : yes/no}}
	doc_bool_dic = {}
	doc_word_list = []
	if type(document) is dict:
		for name in document:
			doc_word_list = document[name].split()
			for word in features:
				if word in doc_word_list:
					features[word]=1
				else:
					features[word]=0
			doc_word_list = []
			doc_bool_dic[name]= features
		return doc_bool_dic
	else:
		doc_word_list = document.split()
		for word in features:
			if word in doc_word_list:
				features[word]=1
			else:
				features[word]=0
		return features	
	
