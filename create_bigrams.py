#!/usr/bin/env python3
# import pickle
import os
from smartdictionary import SmartDictionary

def preprocess(path):
	with open(path, 'r') as file:
		data = file.read().replace('\n', ' ').lower()

	data = data.replace('_', '')
	for c in ['‘','’','’']:
		data = data.replace(c, '\'')

	data = data.replace('\'ll',' _will')
	data = data.replace('\'m',' _am')
	data = data.replace('\'re',' _are')
	data = data.replace('\'ve',' _have')
	data = data.replace('n\'t',' _not')
	data = data.replace('\'s',' _s')
	data = data.replace('\'d',' _d')
	for c in [',','(',')','[',']','"','“',
			'”','-','|','»','«','<','>','—','/']:
		data = data.replace(c,' ')

	for n in ['1','2','3','4','5','6','7','8','9','0']:
		data=data.replace(n,'')

	data = data.replace('\'','')

	for c in ['!','?',';',':']:
		data = data.replace(c,'.')

		return data

fpath = 'training_set/'


# dictionary = {}

# smart_dict = []

# word_len = {}

# for i in range(32):
# 	word_len[i] = 0
# index = 0
# for path in ['wordsEn.txt', 'names.txt']:
# 	f = open(path, 'r')
# 	for l in f:
# 		word = str(l[:-1]).lower()
# 		if not word in smart_dict:
# 				smart_dict.append(word)
# 				dictionary[word] = path
# 		print(index)
# 		index +=1


# 	f.close()

# print(smart_dict)
# index = 0

sd = SmartDictionary(SmartDictionary.SMART_WORDSEN)

fo = open('bigrams.txt', 'w+')

trains = []

for root, dirs, files in os.walk(fpath):
    for file in files:
        if file.endswith(".txt"):
            trains.append(os.path.join(root, file))

print(trains)

to_save = set()

for train in trains:
	print(train)
	book = preprocess(train)
	phrases = book.split('.')

	for p in phrases:
		words = p.split()
		if len(words) > 1:
			if all(sd.check_existance(w) for w in words):
				# self.increment_prior(words[0])
				for i in range(len(words) - 1):
					# self.increment_transition(words[i], words[i+1])
					# self.increment_trans_row(words[i])
					to_save.add('{0}+{1}\n'.format(words[i], words[i+1]))

for item in to_save:
	fo.write(item)

# fo = open('bigrams.txt', 'w+')
# for w1 in smart_dict:
# 	for w2 in smart_dict:
# 		fo.write('{0}+{1}\n'.format(w1, w2))
# 		print(index)
# 		index +=1
fo.close()