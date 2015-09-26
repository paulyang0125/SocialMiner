Documentation Tutorial: SocialMiner
===========================================


What’s Social Miner 
===================

This python-based application is basically to solve the two problems during your day-by-day social network browsing.

1.	You have to spend a lot time reading your friend’s posts one by one, instead of being able to pick them based on your favorite topics. For example, I’m the fan of food, I want to quickly look at the related posts from my friends to know whether they share something useful like restaurant rating or somewhere is interesting and worth to go for grabbing food. 

2.	You’re used to maintaining your connection for friends and families by making comment or like in their pages to show your concern about their status change. So you’re hoping a better and quicker way in getting to know people’s emotional status rather than barely reading their posts one by one.

If you’re suffering from the problems above, Social Miner is just right for you to provide a way to let you view your friend’s post in the categorization-based fashion, such as sport, politician or food in order to make your browsing more fun and efficient and also provide with the sentiment analysis to let you digest all the text-based posts instantly without taking time to read to get what people you care feel about every day.

	
Technical Features
^^^^^^^^^^^^^^^^^^
This python-based application is comprised of two parts – a backend platform supporting REST interface and a frontend by PHP to demonstrate the effects of sentiment analysis and idea clustering. The followings are the supporting features. 


* Chinese text segmentation based on directed acyclic graph with prefix dictionary structure 
* Text preprocessing / feature extraction techniques, such as `BOW`_, `TF-IDF`_ with the dictionary of positive and negative term. 
* Sentient analysis (opinion and subjectivity for Chinese text) based on the algorithms, such as `K-mean`_, `naïve bayes`_, `decision tree`_ and `maximum entropy classification`_
* Ideas clustering based on `latent semantic analysis (LSA)`_ 
* REST interface to access via internet. 


.. _BOW: https://en.wikipedia.org/wiki/Bag-of-words_model
.. _TF-IDF: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
.. _K-mean: https://en.wikipedia.org/wiki/K-means_clustering
.. _naïve bayes: https://en.wikipedia.org/wiki/Naive_Bayes_classifier
.. _decision tree: https://en.wikipedia.org/wiki/Decision_tree
.. _maximum entropy classification: https://en.wikipedia.org/w/index.php?title=Multinomial_logistic_regression&redirect=no
.. _latent semantic analysis (LSA): https://en.wikipedia.org/wiki/Latent_semantic_analysis



SocialMiner documentation contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2
   
   prerequisite
   quickstart
   demo
   apis
   architecture
   limitations
   contributor
   license
   help
   



Indices and tables
==================

* :ref:`search`

