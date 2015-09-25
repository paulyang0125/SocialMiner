# SocialMiner
SocialMiner - the text mining toolkit developed for making sentiment analysis and idea clustering for Chinese text. 

This python-based application is to mainly solve the two problems during your day-by-day social network browsing
Spend a lot of time reading your friend posts word by word in Facebook

-	to find something you’re interesting
-	to know about their emotional status.    

It is comprised of two parts – *a backend platform supporting REST interface* and *a simple frontend by PHP* to demonstrate the effects of sentiment analysis and idea clustering.

Check it out - [**the tutorial doc**]() for how you use Social Miner.



### Quick-start

You can run it on local or remote hosted environment like Amazon
What you need to do
-	Make sure you have [Python 2.7.8 or Anaconda 2.1.0](http://continuum.io/downloads), [MongoDB](https://www.mongodb.org/) installed. 
-	Install all dependent packages by pip
-	Start your mongo database. 
-	Put the frontend with any http server
-	Simply start backend REST server (it support http server already) by the following command 

You can run or modify [*the shell script*]() to ease the booting process of the backend server. 

### Demo
[Live demo for using social miner to browse the facebook post in topic-based fashion and emotional degree for each post](https://chrome.google.com/webstore/detail/social-network-miner/lplokjcgfmgiogkkicgmbdhnnkihbejc)    

You need to login your facebook first and then choose a friend from your friend list. After that, your friend posts will be sorted and display based on the topic they belong and on the left, the emoticons will be used to represent the emotional status of each post.   


### Dependencies

- json
- bottle
- jieba
- pymongo
- nltk
- numpy
- pickle
- scipy
- genism
- heapq
- re

### Limitations

So far Social Miner only supports Chinese text. However, it's easy to alter segmentation for English or other language easily. 


### Contributor:




### License:
The MIT License (MIT) Copyright (c) 2013 Yang Yao-Nien 

Permission is hereby granted, free of charge, to any person obtaining a copy ofthis software and associated documentation files (the "Software"), to deal inthe Software without restriction, including without limitation the rights touse, copy, modify, merge, publish, distribute, sublicense, and/or sell copies ofthe Software, and to permit persons to whom the Software is furnished to do so,subject to the following conditions: The above copyright notice and this permission notice shall be included in allcopies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS ORIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESSFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS ORCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHERIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR INCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



