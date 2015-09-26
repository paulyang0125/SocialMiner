#encoding=utf-8
#!/usr/bin/python


sentiment_options = {}
sentiment_options['simple_data'] = True
sentiment_options['cl_kmeans'] = False
sentiment_options['cl_agglomerative'] = False 
sentiment_options['subjectivity'] = False 
sentiment_options['opinion'] = True
sentiment_options['verbose_all'] = False
sentiment_options['verbose'] = True
sentiment_options['featureExaction_BOW'] = False
sentiment_options['o_crossvalidate'] = 40
sentiment_options['o_testpercentage'] = 20
sentiment_options['cl_naive_bayes'] = True
sentiment_options['cl_decision_tree'] = False 
sentiment_options['cl_max_entropy'] = 'GIS' # "Perform Maximum Entropy classification (provide algorithm: default, GIS, IIS, CG, BFGS, Powell, LBFGSB, Nelder-Mead) "
#myMethods = PreTextProcessingMethods() ## init object 
sentiment_options['double_classify'] = False 
sentiment_options['training'] = False # prediction mode 
