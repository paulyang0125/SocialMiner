Prerequisite and installation
=============================

This is developed based on Python 2.7.8 or Anaconda 2.1.0 and Mongo database. Therefore, for installation 

1.	Please have Python or Anaconda and MongoDB installed and also use pip to install the following required packages before you run social miner.  

-	json
-	bottle
-	jieba
-	pymongo
-	nltk
-	numpy
-	pickle
-	scipy
-	genism
-	heapq
-	re

You can simply install the packages above by performing:: 

	pip install -r requirements.txt
	
2.	Put all files in the folder named frontend in the public folder with any http server, such as www folder in `WAMP server`_ or /var/www in `Linux Apache`_)

.. _WAMP server: http://www.wampserver.com/en/
.. _Linux Apache: http://httpd.apache.org/


3.	Put all files in the folder named backend in somewhere like home folder. 

