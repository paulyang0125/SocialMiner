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
import re, string
from text_mining.preprocess import pre_text_processing
from text_mining.sentiment.sentiment_model import Sentence, BlogMessage
#from optparse import OptionParser
from text_mining.sentiment import featureExaction
from text_mining.sentiment import classification
import pickle
import logging

## LOGGING INIT ##
logger = logging.getLogger('myapp')
#logger.setLevel(logging.DEBUG)
logger.info('SentimentEntry.py started')

#### TODO LIST for v0.0.2 
#### 1. deal with the issue of options mess - too many and hard to control by switch/case 
#### 2. double_classify and which classifier is based on?
#### 3. clustering against training and predict ??  
#### 4. clean the unnecessary control flows and data structures and standardize INPUT/OUTPUT with Restful for sentiment engine... 
#### 5. how to select the right classifier, ex, Naive, SVM or MaxEntropy 
#### 6. Implement more ways of feature exaction ex. TDIDF, most weighted word 
#### 7. add MP and threading for performance improvement

#import config1

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


class Mode:
	MODE_SUBJECTIVE = 1
	MODE_OPINION = 2



class Sentiment:
	options = None
	# posts = None ## segemented post list 
	mypath = None
	used_classifier = None

	def __init__(self, _opinion):
		self.options = _opinion
	
	def training(self, trainingDataPath):
		## TODO v2 implement double classify and implement clustering and also clean unncessary control flows and data stratures 
		logger.info("Go training mode")
		print "Go training mode"
		self.mypath = trainingDataPath
		#allPostsList = pre_text_processing.getXMLData(self.mypath)
		allPostsList = pre_text_processing.getXMLData_multi(self.mypath) ## use multi version to get all *.xml
		messages = self.readXml(allPostsList)
		if (self.options['verbose_all']):
			for msg in messages: logger.debug("original post: \n  %s" % msg ) #print "original post: \n  %s" % msg 

		if self.options['cl_kmeans'] or self.options['cl_agglomerative']: ## TODO
			print "clustering mode doesn't need training, pls use predict mode instead! "
			logger.info("clustering mode doesn't need training, pls use predict mode instead! ")
			exit(1)
		else: 
			#print "classifying mode!"
			logger.info("classifying mode!")
			if self.options['double_classify']: ## TODO
				logger.info("using multiple classifier!")
				#print "using multiple classifier!"
				if (self.options['subjectivity']): results, double_classifier = self.processML(Mode.MODE_SUBJECTIVE, messages) #todo classifier
				elif (self.options['opinion']): results, double_classifier = self.processML(Mode.MODE_OPINION, messages)
				else:
					logger.error("No mode selected use -s or -o. Aborting!")
					print "No mode selected use -s or -o. Aborting!"
					exit(1)
				print results
				save_flag = input("Do you want to save the double classifier? Yes/No ")
				if save_flag == "yes" or save_flag == "YES" or save_flag == "Y":
					if self.saveClassifier(double_classifier):
						logger.info("save double_classifier successfully")
						print "save double_classifier successfully"
			else: 
				print "using single classifier!"
				logger.info("using single classifier!")
				if (self.options['subjectivity']): results, single_classifier = self.processML(Mode.MODE_SUBJECTIVE, messages) #todo classifier
				#elif (self.options['opinion']): results = self.processML(Mode.MODE_OPINION, messages) 
				elif (self.options['opinion']): results, single_classifier = self.processML(Mode.MODE_OPINION, messages)
				else:
					logger.error("No mode selected use -s or -o. Aborting!")
					print "No mode selected use -s or -o. Aborting!"
					exit(1)

				print results
			
				##### use avg of predict tag of sentence for post predict
				logger.info("post's tag:")
				#print "post's tag:"
				for id, msgObj in enumerate(messages):
					print "post " + str(id) + " " + "SentenceNum: {num} Avg: {avg} Sum: {sum}".format( num = msgObj.sentenceNum(), avg = msgObj.getAvgOpinion(), sum = msgObj.getSumOfOpinion())
					logger.info("post " + str(id) + " " + "SentenceNum: {num} Avg: {avg} Sum: {sum}".format( num = msgObj.sentenceNum(), avg = msgObj.getAvgOpinion(), sum = msgObj.getSumOfOpinion()))
					print "original: %s" % msgObj.opinion
					logger.info("original: %s" % msgObj.opinion)
				
				save_flag = raw_input("Do you want to save the classifier? Yes/No ")
				if save_flag == "yes" or save_flag == "YES" or save_flag == "Y" or save_flag == "y":
					self.saveClassifier(single_classifier)
		print "training mode done........ "
		logger.info("training mode done........ ")
		
	def saveClassifier(self, classifier):
		print "saving........"
		#stateFlag = False 
		with open(self.mypath + 'my_classifier.pickle', 'wb') as f:
		#with open('my_classifier.pickle', 'wb') as f: ## Use root as the location to save 
			try:
				pickle.dump(classifier, f)
				#stateFlag = True
				logger.info("save single_classifier successfully")
				print "save single_classifier successfully" 
			except Exception as e:
				logger.error("Failed to save because %s" % e )
				print "Failed to save because %s" % e 
				#return stateFlag
				

	### EX: seg_post = {"p1":["食記 台北 大安 角頭 炙燒 牛排 夜市 價格 水準 妊性 旅行", "童話 人生 痞客 邦"], "p2":["逢甲 夜市 天狗 牛排 炙燒"], "p3":["食記 角頭 炙燒 牛排 藏身 夜市 平價 美食 盈盈 小 站"], "p4":["食譜 煮 義大利麵 上手 義大利","廚房 痞客 邦"]}
	### db_data = {'post_id':[segmented_post,segmented_post]}

	def predict(self, db_data, trainingDataPath):
		print "Go prediction mode"
		logger.info("Go prediction mode")
		self.mypath = trainingDataPath
		if not self.options['cl_kmeans'] or not self.options['cl_agglomerative']:
			self.loadClassifier()
			if not self.used_classifier:
				logger.error("you haven't done the training process for classify, pls do it first!")
				print "you haven't done the training process for classify, pls do it first!"
				exit(1)
		messages = self.readDB(db_data)
		if (self.options['verbose_all']):
			#for msg in messages: 
			for msg in messages[:2]: print "original post: \n %s" % msg ## pick first 2 to save time 
		if (self.options['subjectivity']): stat_all, prediction_tags = self.processML(Mode.MODE_SUBJECTIVE, messages) 
		elif (self.options['opinion']): stat_all	, prediction_tags = self.processML(Mode.MODE_OPINION, messages)
		else:
			print "No mode selected use -s or -o. Aborting!"
			exit (1)
		#print "total number of prediction: %d" % stat_all
		logger.info("total number of prediction: %d" % stat_all)
		#print "prediction_data: \n  %s" % str(prediction_tags)
		logger.info("prediction_data: \n  %s" % str(prediction_tags))
		#print "prediction mode done........ "
		logger.info("prediction mode done........ ")
		#print "post's tag:"
		logger.info("post's tag:")
		resultDic = {}
		#for id, msgObj in enumerate(messages):
		for msgObj in messages:
			print "post " + str(msgObj.id) + " " + "SentenceNum: {num} Avg: {avg} Sum: {sum}".format( num = msgObj.sentenceNum(), avg = msgObj.getAvgOpinion(), sum = msgObj.getSumOfOpinion())
			logger.info("post " + str(msgObj.id) + " " + "SentenceNum: {num} Avg: {avg} Sum: {sum}".format( num = msgObj.sentenceNum(), avg = msgObj.getAvgOpinion(), sum = msgObj.getSumOfOpinion()))
			print "original: %s" % msgObj.opinion
			logger.info("original: %s" % msgObj.opinion)
			## turn the calculated value into the the string tag - pos, neg and Neutr 
			'''
			tag = str()
			if msgObj.getSumOfOpinion() > 0:
				tag = 'Pos'
			elif msgObj.getSumOfOpinion() == 0:
				tag = 'Neutr'
			elif msgObj.getSumOfOpinion() < 0:
				tag = 'Neg'
			else: 
				print "error, at least one tag should be identified!!"
				exit(1)
			resultDic[msgObj.id] = tag
			'''
			resultDic[msgObj.id] = msgObj.getSumOfOpinion()
		print "Return to restful: %s" % str(resultDic)
		logger.info("Return to restful: %s" % str(resultDic))
		return resultDic
		
	def loadClassifier(self):
		print "loading........"
		with open(self.mypath + 'my_classifier.pickle', 'rb') as f:
		#with open('my_classifier.pickle', 'rb') as f:
			try:
				self.used_classifier = pickle.load(f)
				logger.info("loading single_classifier successfully")
				print "loading single_classifier successfully" 
			except Exception as e:
				logger.error("Failed to load because %s" % e)
				print "Failed to load because %s" % e 

	def readDB(self, db_data):
		messages = []
		if self.options['simple_data']: # currently data in mongodb doesn't support, MSG name, user name, rating(push) data .... for v1 FIRST   
			msgRating = 0 ## temp because currently data in mongodb doesn't support  
			msgName = "food" ## temp
			msgUser = "Paul" ## temp
			post_subj = 'na'
			post_obj = 'na'
			for postID, post_list in db_data.iteritems():
				msgRating = 0 ## temp 
				msgSentences = []
				msgID = postID
				for sid, sentence in enumerate(post_list):
					text = sentence
					if isinstance(text, str):
						logger.info('text is a string object, covert it to unicode')
						print 'text is a string object, covert it to unicode'
						text = text.decode("utf-8")
					elif isinstance(text, unicode): 
						logger.info('text is a unicode object')
						print 'text is a unicode object'
					sentId = sid
					if not self.options['training']: ## put na for subj and opnion in predict data 
						subj = 'na'; opinion = 'na'
					senObj = Sentence(text, subj, opinion, sentId)
					msgSentences.append(senObj)
				msgObj = BlogMessage(msgSentences, msgRating, msgUser, msgName, msgID, post_subj, post_obj)
				messages.append(msgObj)
			return messages
		else: # normal data like postDic below [{}, {}, {}] TODO: need to change mongo and restful data 
			logger.info("Not supported yet in version 1")
			print "Not supported yet in version 1"
			exit(-1)
	
### GET XML for training ###
	def readXml(self, allPostsList):
		messages = []
		msgRating = 0
		for postDic in allPostsList:
			msgRating = 0
			msgSentences = []
			msgName = postDic['post.name']
			msgUser = postDic['post.user']
			msgID = postDic['post.id']
			post_subj = postDic['post.pre_subjectivity']
			post_obj = postDic['post.pre_opinion']
			for sentence in postDic['post.sentence']:
				if isinstance(sentence['sentence.text'], str):
					logger.info('text is a string object, covert it to unicode')
					print 'text is a string object, covert it to unicode'
					text = text.decode("utf-8")
				elif isinstance(sentence['sentence.text'], unicode):
					logger.info('text is a unicode object')
					print 'text is a unicode object'
				text = sentence['sentence.text']
				subj = sentence['sentence.subjectivity']
				opinion = sentence['sentence.opinion']
				sentId = sentence['sentence.id']
				s = Sentence(text, subj, opinion, sentId)
				msgSentences.append(s)
			msg = BlogMessage(msgSentences, msgRating, msgUser, msgName, msgID, post_subj, post_obj)
			messages.append(msg)
		return messages

	def processML(self, mode, messages): 
		featureVectors = None; allSentences = None;
		
		# select feature set (one of the alternative values): 
		featureVectors, allSentences = featureExaction.bag_of_words_feature_extractor(mode, messages, self.options)
		print "FV_Num = %d\nFV_Len = %d" % (len(featureVectors), len(featureVectors[0][0]))
		## debug pupose
		if self.options['verbose_all']:
			logger.debug("feature Vector 0 - 10: \n" )
			print "feature Vector 0 - 10: \n" 
			logger.debug(featureVectors[:30])
			print featureVectors[:30]
			logger.debug("first feature vector: \n")
			print "first feature vector: \n"
			logger.debug(str(featureVectors[0]) + "   " + str(allSentences[0].text.encode("utf-8")))
			print str(featureVectors[0]) + "   " + str(allSentences[0].text.encode("utf-8"))
			#print str(featureVectors[0]) + "   " + str(allSentences[0].text) 			
		if (featureVectors == None):
			logger.error("Feature set not selected")
			print "Feature set not selected"
			exit(-1)
		
		## TODO clustering algorithm doesn't need training but need to return prediction data - not implemented yet 
		if self.options['cl_kmeans'] or self.options['cl_agglomerative']:
			return classification.processClustering(mode, featureVectors, allSentences, messages, self.options)
		else:
			if self.options['training']:
				return classification.processClassification(mode, featureVectors, allSentences, messages, self.options)
			else: ## predict
				return classification.processClassification(mode, featureVectors, allSentences, messages, self.options, self.used_classifier)

