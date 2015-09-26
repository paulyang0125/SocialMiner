#encoding=utf-8

'''
SocialMiner
https://github.com/paulyang0125/SocialMiner

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

import requests, json
import os
import csv
from text_mining.preprocess.pre_text_processing import NTUSD


#### Bag of words feature extractor ##########


def bag_of_words_feature_extractor(mode, messages, opt):
	"""
	Bag of words feature exttractor
	There are a few possible options - 
	"""
	if opt['featureExaction_BOW'] == True:
		return bag_of_words_feature_extractor_negation(mode, messages, opt) ### not implemented yet.... 
	else:
		return bag_of_words_feature_extractor_simple(mode, messages, opt)

def bag_of_words_feature_extractor_negation(mode, messages, opt):
	## todo
	return None

def bag_of_words_feature_extractor_simple(mode, messages, opt):
	"""
	Bag of words feature extractor.
	Features are built exclusively from the words found in the incoming messages
	"""
	if opt['verbose']: 
		print "Running bag of words feature selector for mode %d." % mode


	sentences = None
	sentences = getAllSentences(messages) 
		
	### create bag of word  - not gonna to use so far
	### TODO: implement TDIDF here
	'''
	'''
	
	#return assignFeatureVectors(mode, messages, buildbag, opt, False)
	return assignFeatureVectorsSimple(mode, messages, opt)

def getAllSentences(messages):
	ret = []
	for m in messages:
		ret.extend(m.sentences)
	return ret


def assignFeatureVectorsSimple(mode, messages, opt):
	featureVectors = []
	sentences = []
	importtant = u'！ ？ ! ?'
	emoto_pu = set(importtant.split())
	myNTUSD = NTUSD(opt)
	#featureIDMapping = []
	#### [{post_id:"", "senteces":[{sentence_id:featureIndex,} ]} ]
	#posSet, negSet = initNTUSDDics()  #### for ntsud module above for trial
	vectorID = 0
	for msg in messages:
		for senObj in msg.sentences:
			vector = ()
			features = {}
			#myNTUSD = NTUSD()
			if emoto_pu.intersection(senObj.exactPunctuation()):
				#features['contains(emotoPunc)'] = True
				features['emotoPuncNum'] = len(emoto_pu.intersection(senObj.exactPunctuation()))
				#features['contains(%s)' % ep] = True
			#print "search NTUSD by sentence: \n"
			pos_list, neg_list = myNTUSD.exactNTUSDTermByASentence(senObj.getTokenText())
			#pos_list, neg_list = exactNTUSDTermByASentence(s.getTokenText(), posSet, negSet, opt)
			features['numberofpos'] = len(pos_list)
			features['numberofneg'] = len(neg_list)
			features['adjnumber'] = senObj.numAdj()
			#features['vnumber'] = s.numV()
			if mode == 1:
				label = senObj.subjectivity
			elif mode == 2:
				label = senObj.opinion
			vector = (features, label)
			#vector = (features, label, vectorID)
			senObj.assignVectorID(vectorID)
			featureVectors.append(vector)
			vectorID += 1
			if opt['verbose_all']:
				pass
				#print "inside feature vectors" + str(featureVectors)
			sentences.append(senObj)
	return featureVectors, sentences

def document_features(numberofpos, numberofneg, adjnumber, vnumber, punctuation):
	features = {}
	importtant = u'！ ？ ! ?'
	emoto_pu = set(importtant.split())
	for ep in emoto_pu:
		if ep in punctuation:
			features['contains(%s)' % ep] = True 
	features['numberofpos'] = numberofpos
	features['numberofneg'] = numberofneg
	features['adjnumber'] = adjnumber
	features['vnumber'] = vnumber
	return features
	
