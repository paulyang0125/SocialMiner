#encoding=utf-8

import sys
#encoding=utf-8

'''
SocialMiner
https://github.com/paulyang0125/SocialMiner

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

import re
from optparse import OptionParser
import nltk
#from nltk import *
import nltk.cluster
import nltk.cluster.kmeans
import nltk.cluster.gaac
import numpy
from nltk.corpus import movie_reviews
from nltk.corpus import wordnet
#from nltk_contrib.wordnet import *
import pickle
import time
import logging

### TODO 
### 1. how to decide which used_classifier should be used - Naive, SVM ???  
logger = logging.getLogger('myapp')
#logger.setLevel(logging.DEBUG)
logger.info('classification.py started')


def stripLabels(testFeatures):
	"""
	Strips label from a test sentence feature vector
	"""
	return [testFeatures[i][0] for i in range(len(testFeatures))]
	
def selectTrainingTestFeatures(featureVectors, cvstart, cvlength, sentences):
	"""
	Selects training and test feature subsets. 
	Training set is the contingent sublist from location cvstart to cvlength
	"""
	testmappingList = []
	trainmappingList = []
	test = []
	train = []
	#test = [featureVectors[i] for i in range(len(featureVectors)) if cvstart <= i < cvstart + cvlength]
	myindex1 = 0 
	myindex2 = 0 
	for i in range(len(featureVectors)):
		mappingdic = {}
		if cvstart <= i < cvstart + cvlength:
			test.append(featureVectors[i])
			mappingdic["before_ID"] = i
			#mappingdic["after_ID"] = test.index(featureVectors[i])  # index only return the first element that matches
			mappingdic["after_ID"] = myindex1
			testmappingList.append(mappingdic)
			myindex1 += 1
	#train = [featureVectors[i] for i in range(len(featureVectors)) if i < cvstart or cvstart + cvlength <= i]
	for i in range(len(featureVectors)):
		mappingdic = {}
		if i < cvstart or cvstart + cvlength <= i:
			train.append(featureVectors[i])
			mappingdic["before_ID"] = i
			#mappingdic["after_ID"] = train.index(featureVectors[i])
			mappingdic["after_ID"] = myindex2
			trainmappingList.append(mappingdic)
			myindex2 += 1
	testSents = [sentences[i] for i in range(len(featureVectors)) if cvstart <= i < cvstart + cvlength]
	
	assert len(featureVectors) == len(test) + len(train)
	assert len(testSents) == len(test)
	logger.debug("testmappingList:")
	print "testmappingList:"
	logger.debug(testmappingLis)
	print testmappingList
	time.sleep(0.1)
	#print "trainmappingList:"
	#print trainmappingList
	return train, test, testSents, testmappingList

def selectPredictionTestFeatures(featureVectors, sentences):
	
	testmappingList = []
	test = []
	#test = [featureVectors[i] for i in range(len(featureVectors))]
	myindex = 0 
	for i in range(len(featureVectors)):
		mappingdic = {}
		test.append(featureVectors[i])
		mappingdic["before_ID"] = i
		print("exam the feature vector:")
		print (featureVectors[i])
		logger.debug("exam the feature vector:")
		logger.debug(featureVectors[i])
		mappingdic["after_ID"] = myindex
		testmappingList.append(mappingdic)
		myindex += 1
	testSents = [sentences[i] for i in range(len(featureVectors))]
	#print "testmappingList:"
	logger.debug("testmappingList:")
	#print testmappingList
	logger.debug(testmappingList)
	time.sleep(0.1)
	
	return test, testSents, testmappingList
	
def classify_prediction(testFeatures, testSentences, messages, opt, used_classifier, testmappingList):
	#predictedLabelsDic = {}
	testFeaturesD = stripLabels(testFeatures)
	assert (testFeatures != None)
	classifier = used_classifier
	predictedLabels = classifier.batch_classify(testFeaturesD)

	print "start to assign the prediction tag into sentence obj"
	logger.info("start to assign the prediction tag into sentence obj")
	for msgObj in messages:
		for senObj in msgObj.sentences:
			for id, label in enumerate(predictedLabels):
				for test in testmappingList:
					if test["after_ID"] == id and senObj.vector_id == test["before_ID"]:
						if label == "Neutr": senObj.predict_opinion = 0
						elif label == "Neg": senObj.predict_opinion = -1
						elif label == "Pos": senObj.predict_opinion = 1
						else: 
							print "no tag, error!!"
							logger.error("no tag, error!!")

	#for id, labels in enumerate(predictedLabels)
	#vectorIDAssign = lambda n: 'http://www.ptt.cc/bbs/' + board_name + '/index' + str(n) + '.html'
	## assign result to sentenceObj

	assert (len(predictedLabels) == len(testSentences))
	stats_total = len(predictedLabels)
	return (stats_total, predictedLabels)

def classify_training(trainingFeatures, testFeatures, testSentences, messages, opt, testmappingList):
	"""
	Classifies the feature vectos. 
	"""
	assert (trainingFeatures != None and testFeatures != None)

	classifier = None;
	if (opt['cl_naive_bayes']):
		if opt['verbose']: print "Running NaiveBayes classifier"
		classifier = nltk.NaiveBayesClassifier.train(trainingFeatures)
		print "init accuracy for Naive:"
		logger.info("init accuracy for Naive:")
		print nltk.classify.accuracy(classifier, testFeatures)
		logger.info(nltk.classify.accuracy(classifier, testFeatures))
	#### TODO #####
	elif opt['cl_max_entropy'] != None:
		if opt['verbose']:
			logger.info("Running maximum entropy classifier")
			print "Running maximum entropy classifier"
		
		if opt['cl_max_entropy'] == "default": algorithm = None
		else: algorithm = opt['cl_max_entropy']
		traceL=0;
		if opt['verbose']: traceL=3; 
		elif opt['verbose_all']: traceL=5;
		
		classifier = nltk.MaxentClassifier.train(trainingFeatures, algorithm, traceL, max_iter=7)
	elif opt['cl_decision_tree']:
		if opt['verbose']: 
			logger.info("Running decision tree classifier")
			print "Running decision tree classifier"
		classifier = nltk.DecisionTreeClassifier.train(trainingFeatures, entropy_cutoff=0.5, depth_cutoff=70, support_cutoff=10)


	if classifier == None:
		print "No classifier selected! Aborting!"
		logger.error("No classifier selected! Aborting!")
		exit(1)

	testFeaturesD = stripLabels(testFeatures)

	predictedLabels = classifier.batch_classify(testFeaturesD)
	
	## shit.......... 
	print "start to assign the prediction tag into sentence obj"
	logger.info("start to assign the prediction tag into sentence obj")
	for msgObj in messages:
		for senObj in msgObj.sentences:
			for id, label in enumerate(predictedLabels):
				for test in testmappingList:
					if test["after_ID"] == id and senObj.vector_id == test["before_ID"]:
						if label == "Neutr": senObj.predict_opinion = 0
						elif label == "Neg": senObj.predict_opinion = -1
						elif label == "Pos": senObj.predict_opinion = 1
						else: 
							print "no tag, error!!"
							logger.error("no tag, error!!")
	assert (len(predictedLabels) == len(testSentences))
	
		
	stats_total = 0
	stats_correct = 0


	for origFV, newLabel in map(None, testFeatures, predictedLabels):
		origLabel = origFV[1]
		stats_total = stats_total + 1
		if origLabel == newLabel: stats_correct = stats_correct + 1

	if opt['verbose']:
		for l in classifier.labels():
			print "'%s'\t" % l,
			logger.info("'%s'\t" % l,)
		print "L_orig\tL_new"
		logger.info("L_orig\tL_new")

		trainingFeaturesD = stripLabels(trainingFeatures)
		predLabs2 = classifier.batch_classify(trainingFeaturesD)

		
		probcfs = None
		try: 
			probcfs = classifier.batch_prob_classify(trainingFeaturesD)
		except Exception:
			probcfs = ["-" for t in trainingFeaturesD]
			
		for pdist, origFV, newLabel in map(None, probcfs, trainingFeatures, predLabs2):
			origLabel = origFV[1]
			
			for l in classifier.labels():
				if pdist != "-": 
					print "%.3f\t" % pdist.prob(l),
					logger.info("%.3f\t" % pdist.prob(l),)
				else: 
					print "-    \t", 
					logger.info("-    \t",)
			print "  %s\t%s" % (origLabel, newLabel),
			logger.info("  %s\t%s" % (origLabel, newLabel),)
			print ""
			logger.info("")

		
		##### start to use testset with the text showed 
		probcfs = None
		try: 
			probcfs = classifier.batch_prob_classify(testFeaturesD)
		except Exception:
			probcfs = ["-" for t in testFeaturesD]
					
		for pdist, origFV, newLabel, sent in map(None, probcfs, testFeatures, predictedLabels, testSentences):
			origLabel = origFV[1]
			for l in classifier.labels():
				if pdist != "-": 
					print "%.3f\t" % pdist.prob(l),
					logger.info("%.3f\t" % pdist.prob(l),)
				else: 
					print "-    \t",
					logger.info("-    \t",)
			print "  %s\t%s" % (origLabel, newLabel),
			logger.info("  %s\t%s" % (origLabel, newLabel),)
			if opt['verbose_all']: 
				print "\t%s" % sent.text
				logger.debug("\t%s" % sent.text)
			else: 
				print ""
				logger.info("")

	stats_perc = 100.0 * stats_correct / stats_total

	f_measure = evaluateClassificationBCubed([f[1] for f in testFeatures], predictedLabels, opt)

	if opt['verbose']:
		if not (opt['cl_naive_bayes'] or  not opt['cl_max_entropy']):
			classifier.show_most_informative_features()

	return (stats_correct, stats_total, stats_perc, f_measure, classifier, predictedLabels)

def evaluateClassificationBCubed(originalLabels, newLabels, opt):

	label1 = None; label2 = None

	A = 0; B = 0; C = 0; D = 0;
	labelPair = map(None, originalLabels, newLabels)

	precision = 0.0
	recall = 0.0
	for (e1o, e1n) in labelPair:
		sameNew = [ (e2o, e2n) for e2o, e2n in labelPair if e1n == e2n ]  ## same cluster
		sameOld = [ (e2o, e2n) for e2o, e2n in labelPair if e1o == e2o ]  ## same category
		sameBoth = [(e2o, e2n) for e2o, e2n in labelPair if e1o == e2o and e1n == e2n]  ## same cluster and category
		
		precision = precision + 1.0/len(sameNew) * len(sameBoth)
		recall = recall + 1.0/len(sameOld) * len(sameBoth)
		
	precision = precision / len(originalLabels)
	recall = recall / len(originalLabels)

	print precision, recall
	logger.info(precision, recall)
	Fmeasure = 2 * precision * recall / ( precision + recall )
	return Fmeasure



def processClassification(mode, featureVectors, allSentences, messages, options, used_classifier = None):
	if options['training']: 
		print "training mode for Classification!"
		logger.info("training mode for Classification!")
		##featureVectors for training : [({'f1':'','f2':''}, 'Subj'), (), () ]
		crossvalidate = int(1 + 0.01 * len(featureVectors) * float(options['o_crossvalidate']))
		crosslen = int(0.01 * float(options['o_testpercentage']) * len(featureVectors) + 1)

		useCrossvalidation = options['o_crossvalidate'] != -1

		cvstart = 0
		if not useCrossvalidation: 
			cvstart = len(featureVectors) - crosslen
			crossvalidate = crosslen
		results = []
		i = 0
		
		while cvstart < len(featureVectors):

			## divide features in training and test set
			featureTraining, featureTest, testSentences, testmappingList = selectTrainingTestFeatures(featureVectors, cvstart, crosslen, allSentences)
			assert len(featureTraining) > 0 , "There must exist some training features"
			assert len(featureTest) > 0 , "There must exist some test features"

			## perform classification
			## res = tuple - (stats_correct, stats_total, stats_perc, f_measure, classifier)
			res = classify_training(featureTraining, featureTest, testSentences, messages, options, testmappingList)
			used_classifier = res[4] ## this is classifier, gonna save 
			results.append(res)
			print "Run %d. Correct: %d / %d (%5.3f %%) [F = %5.3f] "%(i, res[0], res[1], res[2], res[3])
			logger.info("Run %d. Correct: %d / %d (%5.3f %%) [F = %5.3f] "%(i, res[0], res[1], res[2], res[3]))

			cvstart = cvstart + crossvalidate
			i = i + 1

		return evaluateResults(results, used_classifier)

	else:
		print "prediction mode for Classification!"
		logger.info("prediction mode for Classification!")
		##featureVectors for predict : [({'f1':'','f2':''}, 'na'), (), () ]
		featureTest, testSentences, testmappingList = selectPredictionTestFeatures(featureVectors, allSentences)
		assert len(featureTest) > 0 , "There must exist some test features"
		res = classify_prediction(featureTest, testSentences, messages, options, used_classifier, testmappingList)
		stat_all = res[0]; predict_results = res[1]
		return stat_all , predict_results
	

def evaluateResults(results, used_classifier):
	avg_correct = 0; avg_all = 0; avg_perc = 0; avg_f = 0
	classifiersList = []
	for r in results:
		avg_correct = avg_correct + r[0]
		avg_all = avg_all + r[1] 
		avg_f = avg_f + r[3]
		classifiersList.append(r[4])

	avg_perc = 100.0 * avg_correct / avg_all
	total_runs = len(results)
	avg_correct = avg_correct / total_runs
	avg_f = avg_f / total_runs
	avg_all = avg_all / total_runs
	#saveClassifier(classifiersList)
	print "RESULTS after %d runs" % total_runs
	logger.info("RESULTS after %d runs" % total_runs)
	print "Correct: %d / %d (%5.3f %%) [F = %5.3f]" % (avg_correct, avg_all, avg_perc, avg_f)
	logger.info("Correct: %d / %d (%5.3f %%) [F = %5.3f]" % (avg_correct, avg_all, avg_perc, avg_f))
	# output of process(.)
	return (avg_correct, avg_all, avg_perc, avg_f, used_classifier), used_classifier