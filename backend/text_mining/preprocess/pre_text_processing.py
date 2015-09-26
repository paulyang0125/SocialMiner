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
import jieba, re, string


### global parameters ###
trainingCorpusDirPath = "/home/BBS/fetched/"
boardname = "WomenTalk"
trainingCorpusPath = trainingCorpusDirPath + boardname
pos_dic = "NTUSD/ntusd-positive.txt"
neg_dic = "NTUSD/ntusd-negative.txt"
debug_flag = False
testDict = "dict/dict.txt.big"
jieba.load_userdict(testDict)

import jieba.posseg as pseg


from xml.etree.ElementTree import Element, SubElement, Comment, tostring
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import glob
import logging 
	


## LOGGING INIT ##
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.info('pre_text_processing.py started')

class NTUSD:
	posSet = None
	negSet = None
	opt = None 

	def __init__(self, _opt, _initNTUSD = True):
		self.opt = _opt
		if _initNTUSD:
			self.initNTUSDDics()
	
	def initNTUSDDics(self):
		with open(pos_dic, 'r') as posfile, open(neg_dic, 'r') as negfile:
			self.posSet = set([word.decode("utf-8").rstrip('\r\n') for word in posfile]) ##  using.rstrip('\n') may cause the issue in Linux  
			posfile.seek(0)
			testList = [word.decode("utf-8").rstrip('\r\n') for word in posfile]
			self.negSet = set([word.decode("utf-8").rstrip('\r\n') for word in negfile])
			logger.info('create NTUSD POS / NEG set successfully')
			if self.opt['verbose_all']: 
				logger.debug("check the whole set")
				logger.debug(testList[:50])
			posfile.close()
			negfile.close()

	def exactNTUSDTermByAPost(self, tokenSentenceList): # POST [ SENTENCE, SENTENCE, ] 
		if self.opt['verbose_all']:
			print "exact the emoto terms"
			logger.debug('exact the emoto terms')
		posemotoTermByAPost = []
		negemotoTermByAPost = []
		for eachSentence in tokenSentenceList:
			temp1 = [] ; temp2 = []
			for word in eachSentence:
				if self.opt['verbose_all']: logger.debug("the word to check: %s" % word)
				if word in self.posSet: temp1.append(word)
				elif word in self.negSet: temp2.append(word)
				else: 
					if self.opt['verbose_all']:
						logger.debug("%s is not in NTUSD Dics" % word)
						pass
						#print "%s is not in NTUSD Dics" % word
			posemotoTermByAPost.append(temp1)
			negemotoTermByAPost.append(temp2)
		return posemotoTermByAPost, negemotoTermByAPost
	
	def exactNTUSDTermByASentence(self, tokenSentence):
		if self.opt['verbose_all']:
			print "exact the emoto terms"  
		pos_list = []
		neg_list = []
		#print "token sentence:"
		#print tokenSentence
		#print self.posSet
		for word in tokenSentence:
			if word in self.posSet: 
				pos_list.append(word)
				#print "found pos: %s " % word
			elif word in self.negSet: 
				neg_list.append(word)
				#print "found neg %s " % word
			else:
				#print "%s is not in NTUSD Dics" % word
				if self.opt['verbose_all']:
					pass
					#print "%s is not in NTUSD Dics" % word
		if self.opt['verbose_all']:
			print "pos_list:" + str(pos_list) + " " + str(len(pos_list))
			print "neg_list:" + str(neg_list) + " " + str(len(neg_list))
		return pos_list, neg_list

### module toolboxs 

def makeDicByAPost(self, blog_message): ## blog_message class object 
	tempDic = {}
	tempDic['post.name'] = blog_message.name  # NOT A official getter and setter
	tempDic['post.id'] = blog_message.id
	tempDic['post.user'] = blog_message.user #
	tempDic['post.popularity'] = blog_message.popularity ## push or good in facebook 
	tempDic['post.sentences'] =  [sen.text for sen in blog_message.sentences] ### just for a test... not a office one 
	tempDic["post.subjectivity"] = blog_message.getAvgSubjectivity() ## just for test, only use AVG to determine the post's polarity 
	tempDic["post.opinion"] = blog_message.getAvgOpinion()
	return tempDic
		
def getXMLData(self, xmldoc_path = trainingCorpusPath):
	allPost = []
	os.chdir(trainingCorpusPath)
	tree = ET.ElementTree(file='example.1.try.xml')
	root = tree.getroot()
	## todo ###
	### sentence - text, subjectivity, opinion, numId, 
	### post - numId, user, pre_subjectivity, pre_opinion, rating, postName
	for child_of_post in root:
		sensList = []
		postDic = {}
		if len(child_of_post) > 2: ## not empty 
			if child_of_post[3][0][1].text != 'na': 
				postDic['post.name'] = child_of_post[0].text
				postDic['post.id'] = child_of_post.attrib['num']
				postDic['post.user'] = "paul"
				if len(child_of_post[3]) == 1 and child_of_post[3][0][1].text != 'na':
					postDic['post.pre_subjectivity'] = child_of_post[3][0][1].text
					postDic['post.pre_opinion'] = child_of_post[3][0][2].text
				elif len(child_of_post[3]) > 1 and child_of_post[3][0][1].text != 'na':
					postDic['post.pre_subjectivity'] = child_of_post[1].text
					postDic['post.pre_opinion'] = child_of_post[2].text
				else:
					print "cannot get data out of empty judgement - na"
				for sentence in child_of_post[3]:
					senDic = {}
					senDic['sentence.id'] = sentence.attrib['num']
					senDic['sentence.text'] = sentence[0].text.encode("utf-8").decode("utf-8") #### just covert to utf-8 .. just for test 
					senDic['sentence.subjectivity'] = sentence[1].text
					senDic['sentence.opinion'] = sentence[2].text
					sensList.append(senDic)
				postDic['post.sentence'] = sensList
				allPost.append(postDic)
		else:
			if debug_flag:
				print " element %s fails" % child_of_post.attrib['num']

	return allPost

def post_sentence_segmentation(text_list):
	debug_flag = False
	#for post in text_list:
	afterSegList = jieba.cut(text_list[0], cut_all=False)
	afterText = " ".join(afterSegList)
	#afterText = afterText.encode("utf-8")
	sentenceList = sentence_split(afterText)
	### use unicode in case that NTUSD exaction would fail 
	sentenceList = [sen.decode("utf-8") for sen in sentenceList]
	if debug_flag:
		logger.debug("debug sentenceList: \n")
		#print "debug sentenceList: \n"
		logger.debug(sentenceList)
		#print sentenceList
	if len(sentenceList) > 1: # mean sucessfully split into sentence
		print "sentence segment done... " 
		enderList = sentenceList[1::2]
		sentenceList = [i+j for i,j in zip(sentenceList[0::2],sentenceList[1::2])] # merge odd - text and even - pun ; list[start:end:step].
		sentenceList = [s for s in sentenceList if len(s) > 5] # remove the post where char is not over 5
		#sentenceList = [s for s in sentenceList if len(s) > 5] # remove the post where char is not over 5 
	else: # no ！？。!?～ 
		enderList = []
	#if debug_flag:
	#	print "debug mergedSentencetList: \n"
	#	print sentenceList
	return sentenceList
	
def sentence_split(text):
	#mySeg = re.split(r'\s[！？。!?～]\s', text.encode("utf-8").rstrip('\r\n')) # cover code to ascii to identify the punctuation and add \s to restrict while space
	mySeg = re.split(r'(\s[！？。!?～。！]\s)', text.encode("utf-8").rstrip('\r\n')) # add square to include punctuation like ? 
	#mySeg = re.split(r'(\s[！？。!?～]\s)', text.encode("utf-8")) # add square to include punctuation like ? 
	#mySeg = re.split(r'(\s[！？。!?～]\s)', text) # add square to include punctuation like ? 
	return mySeg
	

### extract only nouns for LSA
def sentence_segmentation_LSA(list_CT_Query):
	segCTStringInAQuery= []
	allLinePerQuery = []
	for line in list_CT_Query:
		out1 = re.sub('[a-zA-Z]+', '', line)       
		out1 = re.sub('[%s]' % re.escape(string.punctuation), '', out1)
		#segline = pseg.cut(out1.decode("utf-8"))
		segline = pseg.cut(out1)
		allLinePerQuery.append(segline)
	for line in allLinePerQuery:
		seglinePerQuery = []
		for z in line:
			#if z.flag == "n" or z.flag == "ns" or z.flag == "v" or z.flag == "a" or z.flag == "nr" or z.flag == "nz" or z.flag == "i" or z.flag == 'l' or z.flag == "vn":
			if z.flag == "n" or z.flag == "ns" or z.flag == "nr" or z.flag == "nz" or z.flag == "i" or z.flag == 'l' or z.flag == "vn":
				seglinePerQuery.append(z.word)
		seglineString = ' '.join(e for e in seglinePerQuery)
		segCTStringInAQuery.append(seglineString)
	return segCTStringInAQuery 	
	
	
	
def makeJsonForSentence(text1):
	tempDic = {}
	tempDic['sentence.segmentedText'] = text1 
	tempDic["sentence.subjectivity"] = ""
	tempDic["sentence.opinion"] = ""
	return tempDic

def getXMLData_multi(self, xmldoc_path = trainingCorpusPath):
	allPost = []
	#allPostDic = {}
	#os.chdir(trainingCorpusPath)
	xml_files = glob.glob(trainingCorpusPath +"/*.xml")
	#xml_element_tree = None
	for xml_file in xml_files:
		tree = ET.ElementTree(file=xml_file)
		root = tree.getroot()
	## TODO for v0.0.2 ###
	### sentence - text, subjectivity, opinion, numId, 
	### post - numId, user, pre_subjectivity, pre_opinion, rating, postName
		for child_of_post in root:
			sensList = []
			postDic = {}
			if len(child_of_post) > 2: ## not empty 
				if child_of_post[3][0][1].text != 'na': 
					postDic['post.name'] = child_of_post[0].text
					postDic['post.id'] = child_of_post.attrib['num']
					postDic['post.user'] = "paul"
					if len(child_of_post[3]) == 1 and child_of_post[3][0][1].text != 'na':
						postDic['post.pre_subjectivity'] = child_of_post[3][0][1].text
						postDic['post.pre_opinion'] = child_of_post[3][0][2].text
					elif len(child_of_post[3]) > 1 and child_of_post[3][0][1].text != 'na':
						postDic['post.pre_subjectivity'] = child_of_post[1].text
						postDic['post.pre_opinion'] = child_of_post[2].text
					else:
						print "cannot get data out of empty judgement - na"
					for sentence in child_of_post[3]:
						senDic = {}
						senDic['sentence.id'] = sentence.attrib['num']
						senDic['sentence.text'] = sentence[0].text.encode("utf-8").decode("utf-8") #### just covert to utf-8 .. just for test 
						senDic['sentence.subjectivity'] = sentence[1].text
						senDic['sentence.opinion'] = sentence[2].text
						sensList.append(senDic)
					postDic['post.sentence'] = sensList
					allPost.append(postDic)
			else:
				if debug_flag:
					print " element %s fails" % child_of_post.attrib['num']

	return allPost
