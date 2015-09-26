#encoding=utf-8

'''
SocialMiner
https://github.com/paulyang0125/SocialMiner
Program:
This program is to start Chinese segmentation, LSA and sentiment 

Copyright (c) 2015 Yao-Nien, Yang
Licensed under the MIT license.
'''

import requests, json


myPost = { "_id": "c108", "POST":{"p1":['為什麼王子的約會裡面的女生動不動就給王子的滅燈呀'],"p2":['我要憑著自己的努力變成內外兼具的小富婆！自己養自己！自己養全家！我可以！！！！'],"p3":['我要無敵了'],"p4":['我們倚賴別人來排遣寂寞，不願跟自己獨處。'],"p5":['原本想說算了！胖就胖～胖子也有胖子的市場！這回兒。。。不瘦不行了'],"p6":['我居然在莉莉外婆家唱家庭式卡啦OK！！唷呼'],"p7":['如果有人的心意讓你猜不透別想了答案就是他(她)沒那麼喜歡你(妳)。'],"p8":['根本就報名不到啊 T_T'],"p9":[ '貧窮並不可怕，可怕的是那顆貧窮慵懶的心。'],"p10":['我明天要變成小黑人了……'],"p11":['我真的不是很喜歡我笑起來特大且詭異的酒窩 =..='],"p12":['我們可以說話整晚不要太早說晚安'],"p13":['如果每次想哭就倒立我大概倒立頭轉大風車樣樣來了吧'],"p14":['我剛剛看到了好多好多完整無誤我前天在台中吃拉麵裡面的玉米XD'],"p15":['無常之間，一切全是身外之物聚散之間，悲歡離合半點不由人到了，都隨花事湮滅……']}}

#mycorpus_url = "http://localhost:8080/mycorpus"
mycorpus_url = "http://173.254.41.118:8080/mycorpus"
ChineseSeg_POST_URL = mycorpus_url + "/" + "chinesesegs" 
ChineseSeg_GET_URL = ChineseSeg_POST_URL + "/" + myPost["_id"]
LSA_POST_URL = mycorpus_url + "/" + "lsa" 
LSA_GET_URL = LSA_POST_URL + "/" + myPost["_id"]
SEN_POST_URL = mycorpus_url + "/" + "sentiment" 
SEN_GET_URL = SEN_POST_URL  + "/" + myPost["_id"]

#ChineseSeg_GET_URL_1 = ChineseSeg_POST_URL + "/" + myPost2["_id"]
#LSA_GET_URL_1 = LSA_POST_URL + "/" + myPost2["_id"]

print "############## Try Chinese segmentation!!! ##############"
print "start to POST : Chinese segmentation"


data = json.dumps(myPost)
print "data:" + "\n", data 
r = requests.post(ChineseSeg_POST_URL, data)

print r.status_code
print r.headers['content-type']


print "Start to GET Chinese segmentation"
r = requests.get(ChineseSeg_GET_URL)
print r.status_code
print r.encoding
a = r.json()

#data1 = json.loads(a)
print "### the segmentation results for LSA ### \n"
for i in a["POST_LSA"].values():
    for s in i:
        print s
		
print "### the segmentation results for sentiment ###\n"
for i in a["POST_sentiment"].values():
    for s in i:
        print s

print "### exam the the received JSON output ###\n"
print a

print "\n"



print "############## Try LSA clustering!!! ############## \n"
### input: {'_id': 1, "_dbid": "doc1"}

print "start to LSA POST \n"
print "test first mode : use _dbid to pick the previous processed segmented data from Chinese seg DB \n"
myLsaPost = {"_id": 1,"_dbid": myPost["_id"]}
data = json.dumps(myLsaPost)
print "data:" + "\n", data
r = requests.post(LSA_POST_URL, data)

print r.status_code
print r.headers['content-type']
if r.status_code == 200:
    print "post sucesses"

else:
    print "connection fails with", r.status_code


print "start to LSA GET\n"
r = requests.get(LSA_GET_URL)
print r.status_code
print r.encoding
a = r.json()


print "### exam the the full JSON output ###\n"
print a

print "\n"


print "############## Try SENTIMENT!!! ##############"


print "start to SENTIMENT POST"
mySenPost = {"_id": 1,"_dbid": myPost["_id"]}
data = json.dumps(mySenPost)
r = requests.post(SEN_POST_URL, data)
print r.status_code
print r.headers['content-type']
if r.status_code == 200:
    print "post sucesses"

else:
    print "connection fails with", r.status_code

print "start to SENTIMENT GET"
r = requests.get(SEN_GET_URL)
print r.status_code
print r.encoding
a = r.json()

print a 

