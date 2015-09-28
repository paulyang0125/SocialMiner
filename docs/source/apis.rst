REST APIs (Draft)
=================

Schema
------

All API access is over HTTPS, and accessed from yourdomain.com (or through http://173.254.41.118:8080/ for demo). All data is sent and received as JSON.



Representations Overview
------------------------

When you fetch a list of resources, the response includes a subset of the attributes for that resource. This is the “summary” representation of the resource.

Chinese segmentation
^^^^^^^^^^^^^^^^^^^^

**Example**: When you want to segement any chinese sentence into a list of words, you need to use
http POST command with sentences you want to apply for.

Input Example(POST)::

	{"_id": "c1", "POST":{"p1":[ u"密胸發動機" ,u"全球快訊" ],"p2":[u"深夜食堂／吉林路尾麵攤 傍晚家鄉味" ,u" 美食-欣傳媒-最好吃" ],"p3":[u"可以食堂說吃一個蘋果!! @ 循環木~大明星 :: 隨意窩 Xuite日誌" ]}}

Syntax::

	POST http://yourdomain:8080/mycorpus/chinesesegs
	
	
**Example**: when you want to retrive the results of Chinese segmentation::
	
	GET http://yourdomain:8080/mycorpus/chinesesegs/_id
	
Idea clustering 
^^^^^^^^^^^^^^^

**Example**: When you want to processs and get the main idea of each sentence you requested (or fb post)

Input Example(POST)::

	{"_id": 1,"_dbid": "c1"} 


Syntax::

	POST http://yourdomain:8080/mycorpus/lsa
	
	GET	http://yourdomain:8080/mycorpus/lsa/_id 
	
	
Sentiment Analysis
^^^^^^^^^^^^^^^^^^

**Example**: When you want to processs and get the sentiment status of each sentence you requested (or fb post)

Input Example (POST)::

	{"_id": 1,"_dbid": "c1"}

Syntax::

	POST http://yourdomain:8080/mycorpus/sentiment
	
	GET	http://yourdomain:8080/mycorpus/sentiment/_id 
	