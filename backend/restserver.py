#encoding=utf-8
'''
SocialMiner
https://github.com/paulyang0125/SocialMiner

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

#### TODO for v0.0.2 
#### 1. deal with the issue of options mess and determine whether the options are open to client
#### 2. add MP and threading for performance improvement


import json
import bottle
import RESTConfigs
from bottle import route, run, request, abort
from pymongo import Connection
import logging
import os
import logging.config
from text_mining.preprocess import pre_text_processing
from text_mining.sentiment.sentiment_config import sentiment_options
from text_mining.sentiment.SentimentEntry import Sentiment
from text_mining.LSA import gensim_lsa_clustering







#### to measure the execution time ####
import time                                                

def timeit(method):

	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()

		print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
		logger.debug('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts))
		return result

	return timed
	
#### main entry ####

#### 0. mongo database connection ####

connection = Connection('localhost', 27017)
db = connection.mydatabase

#### 1. logger init ####
print "initializing the logging ......." 
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(RESTConfigs.logpath)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)
logger.info('REST Server started')


### 2. Chinese segmentation in word  ###
### v1 note: 
### assuming that Chinese sentence segmentation is done by the client  
### 
### Input: 
### {"_cid": "c1", "POST":{"_pid":[],"_pid":[]......,}}  
### Ex: 
###{"_cid": "c1", "POST":{"p1":[ "生物學家揭示鳥類飛行秘密胸發動機" ,"全球快訊" ],"p2":[ "深夜食堂／吉林路尾麵攤 傍晚賣到天亮的家鄉味" ," ###美食｜欣新聞-欣傳媒-最好吃" ], "p3":["可以食堂說吃一個蘋果!! @ 循環木~大明星 :: 隨意窩 Xuite日誌" ]}} 
###
### Process:
###	1. segment the Chinese sentence from client using post_sentence_segmentation() for later sentiment
### analysis
### 2. extract only noun words (they stands for major idea for a sentence) from the segmented sentence ### for later LSA clustering by sentence_segmentation_LSA
### 
 




#output 
#{"_cid": "c1", "POST":{"_pid":[],"_pid":[]......,}}  
#{"_cid": "doc1", "name": "Test Document 1"}

### TODO in version2 ###
### Client send the string of post (is NOT sentence-segmentted and word-segmented) require sentence segmentation and work segmentation
### add _sid for Asynchronous transport
### {"_cid": "c1","_sid":?, "POST":{"_pid":[],"_pid":[]......,}}  
### put different packet with same _cid but different _sid together and deal with the same time   




########################################

@route('/mycorpus/chinesesegs', method='POST')
@timeit
def post_chineseseg():
	#serverInit()
	data = request.body.readline()
	if not data:
		logger.error('400 in POST:chineseseg, no client data received')
		abort(400, 'No data received')
	sent_packet = json.loads(data)
	if not sent_packet.has_key('_id'):
		logger.error('400 in POST:chineseseg, no _id specified')
		abort(400, 'No _id specified')
	## TODO: use _sid to determine if this is a simple or Asynchronous transport
	if sent_packet.has_key('_sid'): 
		return { "success" : False, "error" : "Asynchronous transport is still under implementation!" }
	else: #go the simple transport
		logger.info("Sentence segmentation process")
		results = {}
		results['_id'] = sent_packet['_id']
		results['POST_LSA'] = {}
		results['POST_sentiment'] = {}

		logger.info("Chinese segmentation process for LSA and Sentiment")
		for pid, postText_list in sent_packet["POST"].iteritems():
			
			tempdic_lsa = {}
			tempdic_sentiment = {}
			sentenceList =  pre_text_processing.post_sentence_segmentation(postText_list)
			#logger.info("sentence list: \n %s" % sentenceList)
			## 2 chinese segmentation - one for LSA one for 
			
			segPost_LSA = pre_text_processing.sentence_segmentation_LSA(sentenceList) ## for lsa 
			#segPost_sentiment = chineseseg.chineseSegmentForSentiment(sentenceList) # for sentiment 
			
			tempdic_lsa[pid] = segPost_LSA
			tempdic_sentiment[pid] = sentenceList
			#tempdic_sentiment[pid] = segPost_sentiment
			results['POST_LSA'].update(tempdic_lsa)
			results['POST_sentiment'].update(tempdic_sentiment)
		#logger.info("Chinese Segmentation results : %s" % str(results))
	logger.info("success to complete Chinese segmentation process")
	try:
		db['mycorpus']['chinesesegs'].save(results)
		logger.info("success to save Chinese segmentation results into mongodb")
	#except ValidationError as ve:
	except:
		logger.error('400 in POST:chineseseg, cannot write Chinese segmentation results into mongodb')
		abort(404, 'Cannot write Chinese segmentation results into mongodb!')
		#abort(400, str(ve))
		
		@route('/mycorpus/chinesesegs/:id', method='GET')
@timeit
def get_chineseseg(id):
	logger.info("received id from GET:chinesesegs :  %s " % id)
	entity = db['mycorpus']['chinesesegs'].find_one({'_id':id})
	if not entity:
		logger.error('404 in get:chineseseg, no document with id %s' % id)
		abort(404, 'No document with id %s' % id)
	return entity

# client put(update/create) data  {"_id": "doc1", "name": "Test Document 1"} through http://localhost:8080/documents
# client get(read) though http://localhost:8080/documents/doc1, server returns {"_id": "doc1", "name": "Test Document 1"}
# EX. {"POST":{"p1":[ u"生物學家揭示鳥類飛行秘密胸發動機" ,u"全球快訊" ]}, "_id": "c10"}



########################################
### client input
###
### 2 processes - one to get from DB and another to get segment results from the web request  
###  FIRST MODE: LSA picks the processed data from Chinese segmentation DB
###  {'_id': 1, "_dbid": "doc1"}
###   _dbid is used to track the previous ID  _id is this time ID 
### from DB 
###{u'POST': {u'p2': [u'\u6df1\u591c \u98df\u5802 \u5409\u6797\u8def \u6524 \u5bb6\u9109 \u5473', u'\u7f8e\u98df \u6b23 \u50b3\u5a92 \u597d\u5403'], u'p3': [u'\u98df\u5802 \u8aaa \u5403 \u860b\u679c \u6728\u5927 \u660e\u661f \u7aa9'], u'p1': [u'\u5bc6 \u767c\u52d5\u6a5f', u'\u5168\u7403 \u5feb\u8a0a']}, u'_id': u'c18'}
###  SECOND MODE: client send the segmented post directly to LSA 
###  {"_pid":[],"_pid":[]......,}  
######
### gensim_lsa_clustering.py 
### input: 
### seg_post = {post_id:[segmented_post - unicode string]}
### EX: seg_post = {"p1":["食記 台北 大安 角頭 炙燒 牛排 夜市 價格 水準 妊性 旅行", "童話 人生 痞客 邦"], "p2":["逢甲 夜市 天狗 牛排 炙燒"], "p3":["食記 角頭 炙燒 牛排 藏身 夜市 平價 美食 盈盈 小 站"], "p4":["食譜 煮 義大利麵 上手 義大利","廚房 痞客 邦"]}
### output: post_assignments , topic_assignments
### post_assignments #{'p2': 1, 'p3': 1, 'p1': 1, 'p6': 0, 'p7': 1, 'p4': 0, 'p5': 0, 'p8': 0}### topic_assignments #{0: ['\xe7\xbe\xa9\xe5\xa4\xa7\xe5\x88\xa9\xe9\xba\xb5', '\xe9\x82\xa6', '\xe7\x97\x9e\xe5\xae\xa2', '\xe7\x89\x9b\xe6\x8e\x92'], 1: ['\xe7\xbe\xa9\xe5\xa4\xa7\xe5\x88\xa9\xe9\xba\xb5', '\xe7\x82\x99\xe7\x87\x92', '\xe7\x89\x9b\xe6\x8e\x92', '\xe5\xa4\x9c\xe5\xb8\x82']}
########################################


### _dbid
@route('/mycorpus/lsa', method='POST')
def post_lsa():
	data = request.body.readline()
	if not data:
		logger.error('400 in POST:lsa, no data received')
		abort(400, 'No data received')
	entity = json.loads(data)
	if not entity.has_key('_id'):
		logger.error('400 in POST:lsa, no _id specified')
		abort(400, 'No _id specified')
	#chineseSeg process
	if entity.has_key('_dbid'): ## first mode
		logger.info("LSA picks the processed data from Chinese segmentation DB")
		seg_post = {}
		segEntity = db['mycorpus']['chinesesegs'].find_one({'_id':entity['_dbid']})
		for pid,post in segEntity['POST_LSA'].iteritems():
			seg_post[pid] = post
		## start to LSA clustering 
		mylsa = gensim_lsa_clustering.LSA(RESTConfigs.stopwords, RESTConfigs.ignorechars)
		logger.info("Create LSA clustering")
		mylsa.create_result(seg_post)
		logger.info('Get 2 LSA results')
		post_assignments, topic_assignments = mylsa.get_result()
		result = {}
		#### Use _id rather than _dbid to save result in lsa strusture (control by _dbid)

		result['_id'] = str(entity['_dbid'])
		result['post_assignments'] = post_assignments
		result['topic_assignments'] = topic_assignments
		
		logger.info('show LSA results: \n %s' % str(result))
		#### i did wrong /... KEY must be STRING {0: [u'\u98df\u5802']} -> {'0': [u'\u98df\u5802']}
	
		try:
			db['mycorpus']['lsa'].save(result)
			logger.info("success to save LSA results into mongodb")
		#except ValidationError as ve:
		except: #TODO, except needs to be more specific but validationError doesn't work for bottle now  
			logger.error('404 in POST:lsa, cannot write LSA results into mongodb')
			abort(404, 'Cannot write LSA results into mongodb!')
			#abort(400, str(ve))
	else: #TODO: go the mass transport but not decide how to do yet 
		logger.info("LSA processes the segmented post from Client")
		return { "success" : False, "error" : "sending the segmented post from Client to LSA is still under implementation!" }

@route('/mycorpus/lsa/:id', method='GET')
def get_lsa(id):
	logger.info("received id from GET:lsa :  %s " % id)
	entity = db['mycorpus']['lsa'].find_one({'_id':id}) ##### only support find_one ... no find() alone ... 
	if not entity:
		logger.error('404 in GET:lsa, no document with id %s' % id)
		abort(404, 'No document with id %s' % id)
	return entity

### sentiment analysis ###

@route('/mycorpus/sentiment', method='POST')
def post_sentiment():
	data = request.body.readline()
	if not data:
		logger.error('400 in POST:sentiment, no data received')
		abort(400, 'No data received')
	entity = json.loads(data)
	if not entity.has_key('_id'):
		logger.error('400 in POST:sentiment, no _id specified')
		abort(400, 'No _id specified')
	if entity.has_key('_dbid'): ## first mode
		seg_post = {}
		segEntity = db['mycorpus']['chinesesegs'].find_one({'_id':entity['_dbid']})
		for pid,post in segEntity['POST_sentiment'].iteritems():
			seg_post[pid] = post
		## start to sentiment analysis 
		senObj = Sentiment(sentiment_options)
		predictions = senObj.predict(seg_post, RESTConfigs.trainingFilepath) ## {'p2': 0, 'p3': 0, 'p1': 0, 'p4': 0}
		result = {}
		result['_id'] = str(entity['_dbid'])
		result['sentiment'] = predictions
		logger.info('show the sentiment results: \n %s' % str(result))
		try:
			db['mycorpus']['sentiment'].save(result)
			logger.info("success to save sentiment results into mongodb")
		#except ValidationError as ve: 
		except: ##TODO, except needs to be more specific but validationError doesn't work for bottle now  
			logger.error('404 in POST:sentiment, cannot write sentiment results into mongodb')
			abort(404, 'Cannot write sentiment results into mongodb!')
			#abort(400, str(ve))
	else: ##TODO: go the mass transport but not decide how to do yet 
		return { "success" : False, "error" : "delete not implemented yet" }

@route('/mycorpus/sentiment/:id', method='GET')
def get_sentiment(id):
	entity = db['mycorpus']['sentiment'].find_one({'_id':id}) ##### only support find_one ... no find() alone ... 
	#print entity
	if not entity:
		logger.error('404 in GET:sentiment, no document with id %s' % id)
		abort(404, 'No document with id %s' % id)
	return entity

run(server='paste', host='localhost', port=8080)

