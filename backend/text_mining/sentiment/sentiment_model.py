#encoding=utf-8

'''
SocialMiner
https://github.com/paulyang0125/SocialMiner

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

import jieba, re, string
import os
import jieba.posseg as pseg
import logging


testDict = "dict/dict.txt.big"
jieba.load_userdict(testDict)


#### global parameters ####
delCStr = u'° 《》 （ ）& % ￥ # @ ！ { } 【 】 ？ … ，： 。'
delCStrList = delCStr.split()
excludeSet = set(string.punctuation.decode("utf-8"))
excludeSet.update(delCStrList)
noTERM = u'\u4e0d'
debug_flag = False 

logger = logging.getLogger('myapp')
#logger.setLevel(logging.DEBUG)
logger.info('myData.py started')

class Sentence:

	parent = None
	text = ""
	token_text = None
	pos_number = None
	neg_number = None
	pos_tagged_text = None #(List of Tuple, [('John', 'NNP'), ("'s", 'POS'), ('.', '.')] 
	subjectivity = 0
	opinion = 0
	id = 0
	predict_subjectivity = 0
	predict_opinion = 0
	vector_id = 0
	
	def assignVectorID(self, vectorID):
		self.vector_id = vectorID

	def generatePOSTAG(self):
		""" 
		generate [('John', 'NNP'), ("'s", 'POS')], [('all', 'DT'), ('that', 'DT')]
		"""
		afterSeg = pseg.cut(self.text)
		posttag_list = []
		for w in afterSeg:
			posttag_list.append(tuple([w.word, w.flag]))
		self.pos_tagged_text = posttag_list

	def numAdj(self):
		if self.pos_tagged_text != None:
			return len([w[1] for w in self.pos_tagged_text if w[1] == "a" or w[1]  == "i"])
		else: 
			self.generatePOSTAG()
			return len([w[1] for w in self.pos_tagged_text if w[1] == "a" or w[1]  == "i"]) 

	def numV(self):
		if self.pos_tagged_text != None:
			return len([w[1] for w in self.pos_tagged_text if w[1] == "v"])
		else: 
			self.generatePOSTAG()
			return len([w[1] for w in self.pos_tagged_text if w[1] == "v"])

	def exactPunctuation(self):
		if debug_flag:
			print "exact the punctuation for %d" % self.id
		temp = [w for w in self.text if w in excludeSet]
		pun_list = filter(None, temp) # remove the empty element in the list 
		return pun_list

	def tokenizeText(self):
		s = ''.join(ch for ch in self.text if ch not in excludeSet)
		self.token_text = s.rstrip('\r\n').split()
		if noTERM in self.token_text: ## merge NO Term With the LaterWord
			no_index = self.token_text.index(noTERM)
			self.token_text[no_index:no_index + 2] = [reduce(lambda x, y: x + y, self.token_text[no_index:no_index + 2])]

	def getTokenText(self):
		if self.token_text:
			return self.token_text
		else:
			self.tokenizeText()
			return self.token_text

	def __init__(self, _text, _subjectivity, _opinion, _id):
		self.text = _text
		self.subjectivity = _subjectivity
		self.opinion = _opinion
		self.id = _id
		self.tokenizeText()
		self.token_text = None
		self.pos_number = None
		self.neg_number = None
		
	def __str__(self):
		return "(" + str(self.id) +") " + self.text.encode("utf-8") + " /" + str(self.subjectivity) + "/" +str(self.opinion)
		#return "(" + str(self.id) +") " + self.text + " /" + str(self.subjectivity) + "/" +str(self.opinion)
		
class BlogMessage:

	id = 0
	name = ""
	sentences = []
	popularity = 0
	user = ""
	subjectivity = 0 
	opinion = 0 
	predict_subjectivity = 0 
	predict_opinion = 0
	predict_avg_subjectivity = 0 ## just simple avg by predict in sentence 
	predict_avg_opinion = 0
	#avg_subjectivity = 0
	#avg_opinion = 0

	def sentenceNum(self):
		return len(self.sentences)
	'''
	def getAvgSubjectivity(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.subjectivity
		self.avg_subjectivity =  ret * 1.0 / self.sentenceNum()
		return self.avg_subjectivity

	def getAvgOpinion(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.opinion
		self.avg_opinion =  ret * 1.0 / self.sentenceNum()
		return self.avg_opinion
	'''

	def getAvgSubjectivity(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.predict_subjectivity
		self.predict_avg_subjectivity = float(ret) * 1.0 / float(self.sentenceNum())
		return self.predict_avg_subjectivity
        
	def getAvgOpinion(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.predict_opinion
		self.predict_avg_opinion = float(ret) * 1.0 / float(self.sentenceNum())
		return self.predict_avg_opinion

	def getSumOfOpinion(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.predict_opinion
		## TODO classigy second time
		return ret
		
	def getSumOfSubjectivity(self):
		if self.sentenceNum() == 0: return 0
		ret = 0
		for s in self.sentences:
			ret = ret + s.predict_subjectivity
		## TODO classigy second time
		return ret

	def __init__(self, _sentences, _popularity, _user, _name, _numId, _subj, _obj):
		self.popularity = _popularity
		self.user = _user
		self.sentences = _sentences
		self.name = _name
		self.id = _numId
		self.subjectivity = _subj
		self.opinion = _obj
		for s in self.sentences:
			s.parent = self

	def __str__(self):
		s = "[" + self.user + "][" + str(self.popularity) + "]\n"
		#s = "\n".join([s.__str__() for s in self.sentences])
		s = s + "\n".join(map(str, self.sentences))
		s = s + "\n--------\n"
		return s