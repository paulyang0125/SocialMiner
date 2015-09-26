Quick Start
===========

Setup the backend
^^^^^^^^^^^^^^^^^

Assuming you have installed all the above in the **home** folder, the first thing you needs to do is to start MongoDB by::

	$nohup /home/mongodb-linux-x86_64-2.4.4/bin/mongod --dbpath /home/mongodata/db/


Then you can start the backend server by the command below::

	$nohup python /home/backend/restserver.py
	
If the server works normally, you will see the following messages indicating the http server – “bottle” is working and waiting to respond client’s request::

	2015-09-25 18:38:41,789 : INFO : gensim_lsa_clustering.py started
	Building Trie..., from /home/backend/dict/dict.txt.big
	loading model from cache /tmp/jieba.user.5689562627647743447.cache
	loading model cost  2.00677394867 seconds.
	Trie has been built succesfully.
	2015-09-25 18:38:47,550 : INFO : pretextprocess.py started
	2015-09-25 18:38:51,570 : INFO : classification.py started
	2015-09-25 18:38:51,570 : INFO : sentimententry.py started
	2015-09-25 18:38:51,580 : INFO : Server started
	Bottle v0.11.6 server starting up (using WSGIRefServer())...
	Listening on http://173.254.41.118:8080/
	Hit Ctrl-C to quit.
	
You can also simply run the shell script – `startbackend.sh`_ to automatically initialize your MongoDB and the backend server::

	$bash utilities/startbackend.sh
	
.. _startbackend.sh:



The following message in the console indicates the initiation works::
	
	Kill the related processes
	Start MongoDB
	Wait 5 secs until MongoDB starts
	nohup: redirecting stderr to stdout
	bash startbackend.sh Start REST server
	Done, use PS and tail to check the status of the server!
	Search the processes from PS and show their status
	MongoDB Running!
	REST server Running!

You can run the commands like ps or top to check if the processes – *mongod* and *python* are working::

	$ ps aux
	
	USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
	thecity4 13686  0.0  0.0  11656  1784 pts/0    S    18:37   0:00 -bash
	thecity4 23493  0.3  0.1 348472 38420 pts/0    Sl   18:43   0:07 /home/mongodb-linux-x86_64-2.4.4/bin/mongod --dbpath /home/mongodata/db/
	thecity4 23608  0.4  2.3 974056 668832 pts/0   S    18:43   0:09 python /home/backend/restserver.py
	thecity4 29121  0.0  0.0  13376  1032 pts/0    R+   19:20   0:00 ps aux

You can also check the log by running the command to know about the server initialization status::

	$cat rest_log/server_init.log
	
	2015-09-25 18:38:41,789 : INFO : gensim_lsa_clustering.py started
	Building Trie..., from /home/backend/dict/dict.txt.big
	loading model from cache /tmp/jieba.user.5689562627647743447.cache
	loading model cost  2.00677394867 seconds.
	Trie has been built succesfully.
	2015-09-25 18:38:47,550 : INFO : pretextprocess.py started
	2015-09-25 18:38:51,570 : INFO : classification.py started
	2015-09-25 18:38:51,570 : INFO : sentimententry.py started
	2015-09-25 18:38:51,580 : INFO : Server started
	Bottle v0.11.6 server starting up (using WSGIRefServer())...
	Listening on http://173.254.41.118:8080/
	Hit Ctrl-C to quit.

Note that if your MongoDB, its database file and the backend are installed in the different location, you need to modify the executing path in *startbackend.sh*

Now it’s time to do the quick test for the backend. 

You can simply run the utility called *clienttest.py* which is basically to simulate the frontend’s behavior to test whether the REST and the relevant features – Chinese segmentation, LSA and sentiment from the backend server work or not. However, notice that you need to change **mycorpus_url** according to your server IP or URL before you start *clienttest.py*.

If you can see the results above, that means the backend server works now::

	$python tests/clienttest.py
	
	############## Try Chinese segmentation!!! ##############
	start to POST : Chinese segmentation
	data:
	{"POST": {"p10": ["\u6211\u660e\u5929\u8981\u8b8a\u6210\u5c0f\u9ed1\u4eba\u4e86\u2026\u2026"], "p11": ["\u6211\u771f\u7684\u4e0d\u662f\u5f88\u559c\u6
	b61\u6211\u7b11\u8d77\u4f86\u7279\u5927\u4e14\u8a6d\u7570\u7684\u9152\u7aa9 =..="], "p12": ["\u6211\u5011\u53ef\u4ee5\u8aaa\u8a71\u6574\u665a\u4e0d\u
	8981\u592a\u65e9\u8aaa\u665a\u5b89"], "p13": ["\u5982\u679c\u6bcf\u6b21\u60f3\u54ed\u5c31\u5012\u7acb\u6211\u5927\u6982\u5012\u7acb\u982d\u8f49\u5927
	\u98a8\u8eca\u6a23\u6a23\u4f86\u4e86\u5427"], "p14": ["\u6211\u525b\u525b\u770b\u5230\u4e86\u597d\u591a\u597d\u591a\u5b8c\u6574\u7121\u8aa4\u6211\u52
	4d\u5929\u5728\u53f0\u4e2d\u5403\u62c9\u9eb5\u88e1\u9762\u7684\u7389\u7c73XD"], "p15": ["\u7121\u5e38\u4e4b\u9593\uff0c\u4e00\u5207\u5168\u662f\u8eab
	\u5916\u4e4b\u7269\u805a\u6563\u4e4b\u9593\uff0c\u60b2\u6b61\u96e2\u5408\u534a\u9ede\u4e0d\u7531\u4eba\u5230\u4e86\uff0c\u90fd\u96a8\u82b1\u4e8b\u6e6
	e\u6ec5\u2026\u2026"], "p2": ["\u6211\u8981\u6191\u8457\u81ea\u5df1\u7684\u52aa\u529b\u8b8a\u6210\u5167\u5916\u517c\u5177\u7684\u5c0f\u5bcc\u5a46\uff
	01\u81ea\u5df1\u990a\u81ea\u5df1\uff01\u81ea\u5df1\u990a\u5168\u5bb6\uff01\u6211\u53ef\u4ee5\uff01\uff01\uff01\uff01"], "p3": ["\u6211\u8981\u7121\u6
	575\u4e86"], "p1": ["\u70ba\u4ec0\u9ebc\u738b\u5b50\u7684\u7d04\u6703\u88e1\u9762\u7684\u5973\u751f\u52d5\u4e0d\u52d5\u5c31\u7d66\u738b\u5b50\u7684\u
	6ec5\u71c8\u5440"], "p6": ["\u6211\u5c45\u7136\u5728\u8389\u8389\u5916\u5a46\u5bb6\u5531\u5bb6\u5ead\u5f0f\u5361\u5566OK\uff01\uff01\u5537\u547c"], "
	p7": ["\u5982\u679c\u6709\u4eba\u7684\u5fc3\u610f\u8b93\u4f60\u731c\u4e0d\u900f\u5225\u60f3\u4e86\u7b54\u6848\u5c31\u662f\u4ed6(\u5979)\u6c92\u90a3\u
	9ebc\u559c\u6b61\u4f60(\u59b3)\u3002"], "p4": ["\u6211\u5011\u501a\u8cf4\u5225\u4eba\u4f86\u6392\u9063\u5bc2\u5bde\uff0c\u4e0d\u9858\u8ddf\u81ea\u5df
	1\u7368\u8655\u3002"], "p5": ["\u539f\u672c\u60f3\u8aaa\u7b97\u4e86\uff01\u80d6\u5c31\u80d6\uff5e\u80d6\u5b50\u4e5f\u6709\u80d6\u5b50\u7684\u5e02\u58
	34\uff01\u9019\u56de\u5152\u3002\u3002\u3002\u4e0d\u7626\u4e0d\u884c\u4e86"], "p8": ["\u6839\u672c\u5c31\u5831\u540d\u4e0d\u5230\u554a T_T"], "p9": [
	"\u8ca7\u7aae\u4e26\u4e0d\u53ef\u6015\uff0c\u53ef\u6015\u7684\u662f\u90a3\u9846\u8ca7\u7aae\u6175\u61f6\u7684\u5fc3\u3002"]}, "_id": "c108"}
	200
	text/html; charset=UTF-8
	Start to GET Chinese segmentation
	200
	None
	### the segmentation results for LSA ###

	富婆 全家

	王子 女生 王子
	外婆家 家庭式 卡啦
	心意 答案

	原本 胖子 胖子

	心
	黑人

	晚安
	頭
	玉米
	身外之物 人 隨花 事
	### the segmentation results for sentiment ###

	我要 憑著 自己 的 努力 變成 內外 兼具 的 小 富婆 ！ 自己 養 自己 ！ 自己 養 全家 ！ 我 可以 ！ ！ ！ ！
	我要 無敵 了
	為什麼 王子 的 約會 裡面 的 女生 動不動 就給 王子 的 滅燈 呀
	我 居然 在 莉莉 外婆家 唱 家庭式 卡啦 OK ！ ！ 唷 呼
	如果 有人 的 心意 讓 你 猜不透 別想 了 答案 就是 他 ( 她 ) 沒 那麼 喜歡 你 ( 妳 ) 。
	我們 倚賴 別人 來 排遣 寂寞 ， 不願 跟 自己 獨處 。
	原本 想 說 算了 ！ 胖 就 胖 ～ 胖子 也 有 胖子 的 市場 ！ 這回 兒 。 。 。 不瘦 不行 了
	根本 就 報名 不到 啊 T _ T
	貧窮 並不 可怕 ， 可怕 的 是 那顆 貧窮 慵懶 的 心 。
	我 明天 要 變成 小 黑人 了 … …
	我 真的 不是 很 喜歡 我笑 起來 特大 且 詭異 的 酒窩 = .. =
	我們 可以 說話 整晚 不要 太早 說 晚安
	如果 每次 想 哭 就 倒立 我 大概 倒立 頭轉 大風車 樣樣 來 了 吧
	我 剛剛 看到 了 好多好多 完整 無誤 我 前天 在 台 中 吃 拉 麵 裡面 的 玉米 XD
	無常 之間 ， 一切 全是 身外之物 聚散 之間 ， 悲歡離合 半點 不由 人到 了 ， 都 隨花 事 湮滅 … …
	### exam the the received JSON output ###

	{u'POST_sentiment': {u'p2': [u'\u6211\u8981 \u6191\u8457 \u81ea\u5df1 \u7684 \u52aa\u529b \u8b8a\u6210 \u5167\u5916 \u517c\u5177 \u7684 \u5c0f \u5bcc
	\u5a46 \uff01 \u81ea\u5df1 \u990a \u81ea\u5df1 \uff01 \u81ea\u5df1 \u990a \u5168\u5bb6 \uff01 \u6211 \u53ef\u4ee5 \uff01 \uff01 \uff01 \uff01'], u'p3
	': [u'\u6211\u8981 \u7121\u6575 \u4e86'], u'p1': [u'\u70ba\u4ec0\u9ebc \u738b\u5b50 \u7684 \u7d04\u6703 \u88e1\u9762 \u7684 \u5973\u751f \u52d5\u4e0d
	\u52d5 \u5c31\u7d66 \u738b\u5b50 \u7684 \u6ec5\u71c8 \u5440'], u'p6': [u'\u6211 \u5c45\u7136 \u5728 \u8389\u8389 \u5916\u5a46\u5bb6 \u5531 \u5bb6\u5e
	ad\u5f0f \u5361\u5566 OK \uff01 \uff01 \u5537 \u547c'], u'p7': [u'\u5982\u679c \u6709\u4eba \u7684 \u5fc3\u610f \u8b93 \u4f60 \u731c\u4e0d\u900f \u52
	25\u60f3 \u4e86 \u7b54\u6848 \u5c31\u662f \u4ed6 ( \u5979 ) \u6c92 \u90a3\u9ebc \u559c\u6b61 \u4f60 ( \u59b3 ) \u3002'], u'p4': [u'\u6211\u5011 \u501
	a\u8cf4 \u5225\u4eba \u4f86 \u6392\u9063 \u5bc2\u5bde \uff0c \u4e0d\u9858 \u8ddf \u81ea\u5df1 \u7368\u8655 \u3002'], u'p5': [u'\u539f\u672c \u60f3 \u
	8aaa \u7b97\u4e86 \uff01 \u80d6 \u5c31 \u80d6 \uff5e \u80d6\u5b50 \u4e5f \u6709 \u80d6\u5b50 \u7684 \u5e02\u5834 \uff01 \u9019\u56de \u5152 \u3002 \u
	3002 \u3002 \u4e0d\u7626 \u4e0d\u884c \u4e86'], u'p8': [u'\u6839\u672c \u5c31 \u5831\u540d \u4e0d\u5230 \u554a T _ T'], u'p9': [u'\u8ca7\u7aae \u4e26
	\u4e0d \u53ef\u6015 \uff0c \u53ef\u6015 \u7684 \u662f \u90a3\u9846 \u8ca7\u7aae \u6175\u61f6 \u7684 \u5fc3 \u3002'], u'p10': [u'\u6211 \u660e\u5929 \
	u8981 \u8b8a\u6210 \u5c0f \u9ed1\u4eba \u4e86 \u2026 \u2026'], u'p11': [u'\u6211 \u771f\u7684 \u4e0d\u662f \u5f88 \u559c\u6b61 \u6211\u7b11 \u8d77\u4
	f86 \u7279\u5927 \u4e14 \u8a6d\u7570 \u7684 \u9152\u7aa9 = .. ='], u'p12': [u'\u6211\u5011 \u53ef\u4ee5 \u8aaa\u8a71 \u6574\u665a \u4e0d\u8981 \u592a
	\u65e9 \u8aaa \u665a\u5b89'], u'p13': [u'\u5982\u679c \u6bcf\u6b21 \u60f3 \u54ed \u5c31 \u5012\u7acb \u6211 \u5927\u6982 \u5012\u7acb \u982d\u8f49 \u
	5927\u98a8\u8eca \u6a23\u6a23 \u4f86 \u4e86 \u5427'], u'p14': [u'\u6211 \u525b\u525b \u770b\u5230 \u4e86 \u597d\u591a\u597d\u591a \u5b8c\u6574 \u7121
	\u8aa4 \u6211 \u524d\u5929 \u5728 \u53f0 \u4e2d \u5403 \u62c9 \u9eb5 \u88e1\u9762 \u7684 \u7389\u7c73 XD'], u'p15': [u'\u7121\u5e38 \u4e4b\u9593 \uff
	0c \u4e00\u5207 \u5168\u662f \u8eab\u5916\u4e4b\u7269 \u805a\u6563 \u4e4b\u9593 \uff0c \u60b2\u6b61\u96e2\u5408 \u534a\u9ede \u4e0d\u7531 \u4eba\u523
	0 \u4e86 \uff0c \u90fd \u96a8\u82b1 \u4e8b \u6e6e\u6ec5 \u2026 \u2026']}, u'_id': u'c108', u'POST_LSA': {u'p2': [u'\u5bcc\u5a46 \u5168\u5bb6'], u'p3'
	: [u''], u'p1': [u'\u738b\u5b50 \u5973\u751f \u738b\u5b50'], u'p6': [u'\u5916\u5a46\u5bb6 \u5bb6\u5ead\u5f0f \u5361\u5566'], u'p7': [u'\u5fc3\u610f \
	u7b54\u6848'], u'p4': [u''], u'p5': [u'\u539f\u672c \u80d6\u5b50 \u80d6\u5b50'], u'p8': [u''], u'p9': [u'\u5fc3'], u'p10': [u'\u9ed1\u4eba'], u'p11':
	 [u''], u'p12': [u'\u665a\u5b89'], u'p13': [u'\u982d'], u'p14': [u'\u7389\u7c73'], u'p15': [u'\u8eab\u5916\u4e4b\u7269 \u4eba \u96a8\u82b1 \u4e8b']}}



	############## Try LSA clustering!!! ##############

	start to LSA POST

	test first mode : use _dbid to pick the previous processed segmented data from Chinese seg DB

	data:
	{"_id": 1, "_dbid": "c108"}
	200
	text/html; charset=UTF-8
	post sucesses
	start to LSA GET

	200
	None
	### exam the the full JSON output ###

	{u'topic_assignments': {u'1': [u'\u5bcc\u5a46', u'\u5168\u5bb6', u'\u5fc3\u610f', u'\u5916\u5a46\u5bb6'], u'0': [u'\u982d', u'\u9ed1\u4eba', u'\u5fc3
	', u'\u7389\u7c73'], u'2': [u'\u7389\u7c73', u'\u738b\u5b50', u'\u80d6\u5b50', u'\u665a\u5b89']}, u'post_assignments': {u'p2': 1, u'p3': u'NB', u'p1'
	: 2, u'p6': 0, u'p7': 0, u'p4': u'NB', u'p5': 2, u'p8': u'NB', u'p9': 0, u'p10': 0, u'p11': u'NB', u'p12': 2, u'p13': 0, u'p14': 2, u'p15': 2}, u'_id
	': u'c108'}


	############## Try SENTIMENT!!! ##############
	start to SENTIMENT POST
	200
	text/html; charset=UTF-8
	post sucesses
	start to SENTIMENT GET
	200
	None
	{u'_id': u'c108', u'sentiment': {u'p2': 0, u'p3': 0, u'p1': 0, u'p6': 0, u'p7': 0, u'p4': 0, u'p5': 0, u'p8': 0, u'p9': -1, u'p10': 0, u'p11': 0, u'p
	12': 0, u'p13': 0, u'p14': 0, u'p15': 0}}


You can also observe the server operations on the fly or debug by running the command below:: 

	$tail -f rest_log/restinfo.log



Setup the frontend
^^^^^^^^^^^^^^^^^^

You simply make sure you put all frontend codes in **www folder** and start your htttp server before open index.php by any your favorite browser. 

In the case of demo, the full URL is:: 

	http://173.254.41.118/leon/prototype_for_Common/index.php

Then you can see the login screen below

.. image:: login.GIF

