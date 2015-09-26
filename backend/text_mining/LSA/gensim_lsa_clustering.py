# coding: utf-8

'''
SocialMiner
https://github.com/paulyang0125/SocialMiner

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
from gensim import corpora, models, similarities
from gensim.matutils import corpus2dense, corpus2csc

from scipy.odr import models
import unittest, os, os.path, tempfile, inspect

import numpy
import gensim
import logging
import re

from gensim.corpora import mmcorpus, Dictionary
from gensim.models import lsimodel, ldamodel, tfidfmodel, rpmodel, logentropy_model, TfidfModel, LsiModel
from gensim import matutils,corpora
from heapq import nlargest

logger = logging.getLogger('myapp')
logger.info('gensim_lsa_clustering.py started')

### target 
### input: 
### seg_post = {post_id:[segmented_post - unicode string]}
### Ex. {"p1":["食記 台北 大安 角頭 炙燒 牛排 夜市 價格 水準 妊性 旅行 童話 人生 痞客 邦", "逢甲 夜市 天狗 牛排 炙燒"], "p2":["食記 角頭 炙燒 牛排 藏身 夜市 平價 美食 盈盈 小 站","食譜 煮 義大利麵 上手 義大利 廚房 痞客 邦",]
### stopwords
### ignorechars

### Output:
### post_assignment = {post_id:topic} Ex. {"p1":"t1"}
### topics = {topic_id:[keywords]} Ex. {"t1":["秘密", "飛行器", "新華", "任務"] 



### Global parameters ###
testFolder = "log/lsa_log/"
testDictionary = testFolder + 'all.dict'
testDictionaryString = testFolder + "all.dict.string"
testBOWCorpus = testFolder + "all.mm"
testIndex = testFolder + "all.index"
ignorechars = ''',:'!'''
stopword_path = "dict/stopwords-utf8.txt"





#### model process ######

class LSA(object):
	def __init__(self, stopwords, ignorechars):
		#self.stopwords = stopwords
		self.ignorechars = ignorechars
		self.wdict = {} 
		self.dcount = 0
	def createStopwords(self, stopword_path):
		with open(stopword_path, 'r') as file1:
			temp = file1.read()
			self.stopwords = temp.split()

	def parse_dic_bow(self, seg_post):
		self.posts = [post for post in seg_post.values()]
		logger.info("BOW process... ")
		print "original post:"
		logger.debug("original post:")
		logger.debug(self.posts)
		#print self.posts
		self.mergeLineForOnePost = [" ".join(post) for post in self.posts] #change to ['\xe9\xa3\x9f\xe8\xa8\x98 \xe8\xa7\x92\xe9\xa0\xad',' efffe wedw'] 
		#print self.mergeLineForOnePost
		#self.texts = [[word for word in post.split()] for post in self.mergeLineForOnePost] #change to [['human', 'interface', 'computer'],['survey', 'user']]
		## covert UTF to ASCII
		self.texts = [[word.encode('utf8') for word in post.split()] for post in self.mergeLineForOnePost] #change to [['human', 'interface', 'computer'],['survey', 'user']]
		print "self.mergeLineForOnePost: "
	
		self.dictionary = gensim.corpora.Dictionary(self.texts)


		self.postIdList = [str(postId) for postId in seg_post.keys()]
		logger.debug("original dic and list:")
		logger.debug(self.dictionary, len(self.dictionary), self.postIdList)
		print "original dic and list:"
		print self.dictionary, self.postIdList

		### preprocess - remove the once-word, stopwords, other shits 
		stop_ids = [self.dictionary.token2id[stopword] for stopword in self.stopwords if stopword in self.dictionary.token2id]
		once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.iteritems() if docfreq == 1]
		### remove once_id sometime cause invalid shape of LSA (TOO LESS words to cluster)
		
		#self.dictionary.filter_tokens(once_ids)
		self.dictionary.filter_tokens(stop_ids)
		logger.info("removed once-words and stopwords......")
		logger.debug(self.dictionary, len(self.dictionary))
		print "removed once-words and stopwords......"
		print self.dictionary
		self.dictionary.compactify()
		self.new_vec = [self.dictionary.doc2bow(post) for post in self.texts]
		#self.new_vec = self.dictionary.doc2bow(post for post in self.coverts)
	def store(self):
		logger.info("store process starts")
		self.dictionary.save(testDictionary)
		self.dictionary.save_as_text(testDictionaryString)
		corpora.MmCorpus.serialize(testBOWCorpus, self.new_vec) # store to disk, for later use
		#corpus = corpora.MmCorpus(testBOWCorpus) # comes from the store 
		#dictionary = corpora.Dictionary.load(testDictionary) # comes from the store
	def TFIDF(self):
		logger.info("TFIDF process starts")
		self.tfidf = TfidfModel(self.new_vec)
		self.corpus_tfidf = self.tfidf[self.new_vec]
	def printInfo(self):
		print 'show Dic: '
		print self.dictionary
		print 'show BOW: '
		for bow in self.new_vec: 
			print bow
		print 'show corpus_tfidf model: '
		print self.tfidf
		print "show corpus_tfidf: "
		for i in self.corpus_tfidf:
			print i
		print "show LSA assignment of each post: "
		#self.num = len(self.corpus_lsi)
		#for doc, i in zip(self.corpus_lsi, range(self.num)): # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
		for doc, postId in zip(self.corpus_lsi,self.postIdList):
			templist = [] 
			print 'post: {0}'.format(postId)
			print doc
			#print "breakdown"
			#for each in doc:
			#	templist.append(abs(each[1]))
			#print "templist: "
			#print templist
			theLarge = nlargest(1, doc, key=lambda e:abs(e[1])) ## 1 means find the largest one
			if theLarge:
				print "the largest one with absoule value: ", theLarge[0][0]
			else:
				print "cannot find it!!!!"
		print "LSA Topics : "
		print self.topics
		print "Break down : "
		for i in self.topics:
			print i
			print type(i)
	def build(self):
		### need to find out a way to pick the proper number of the cluster - may be based on the number of POST 
		self.lsi_model = LsiModel(self.corpus_tfidf, id2word = self.dictionary, num_topics=3)
		self.corpus_lsi = self.lsi_model[self.corpus_tfidf]
		##self.topics = self.lsi_model.print_topics(num_topics=5, num_words=4)
		#print "topics difference"
		#print self.lsi_model.print_topic(2, topn=4)
		self.topics = self.lsi_model.show_topics(num_topics=5, num_words=4, log=False, formatted=False)
		#print "tuple!@!"
		#print ss 
	def repaserForOutput(self): 
	### post_assignment = {post_id:topic} Ex. {"p1":"t1"}
	### topic_assignment = {topic_id:[keywords]} Ex. {"t1":["秘密", "飛行器", "新華", "任務"]
		#print "start to extact info for post_assignment"
		self.post_assignment = {}
		self.topic_assignment = {}
		for doc, postId in zip(self.corpus_lsi,self.postIdList): #self.postIdList // ['p2', 'p3', 'p1', 'p6', 'p7', 'p4', 'p5', 'p8']
			theTopic = nlargest(1, doc, key=lambda e:abs(e[1]))
			if theTopic:
				self.post_assignment[postId] = theTopic[0][0]
			else: 
				self.post_assignment[postId] = "NB"
			#self.post_assignment[postId] = theTopic[0]
		self.num = len(self.topics)
		for topic, num in zip(self.topics, range(self.num)):
			topicWords = []
			for each in topic:
				#covert from string to unicode
				topicWords.append(each[1].decode('utf8'))
				#topicWords.append(each[1])
			## just exact the first topic content, for example, use "秘密" in ["秘密", "飛行器", "新華", "任務"]
			#self.topic_assignment[str(num)] = topicWords[0]
			self.topic_assignment[str(num)] = topicWords
		#matchObj = re.match( r'(.*) are(\.*)', line)
		#rerurn(self.post_assignment,self.topic_assignment)
		return (self.post_assignment,self.topic_assignment)
	def create_result(self,seg_post):
		logger.info('LSA main process starts.....')
		self.createStopwords(stopword_path)
		self.parse_dic_bow(seg_post)
		self.TFIDF()
		self.build()
		self.store()
	def get_result(self):
		self.printInfo()
		return (self.repaserForOutput())
		

		
#### controller process (just for test, implemented in RestAPI) ###### 
