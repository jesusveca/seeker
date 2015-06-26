import re
#Nltk
import queue as Q
import nltk

import glob
import numpy as np

from pprint import pprint
import read_write_json
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer

class PreProcessManager(object):
    def __init__(self):
        self.json_obj = read_write_json.JsonManagePsql()
        # self.data_new = self.json_obj.read_json_file("espectaculos.json")
        # #data_new = {"los angeles times","new york post","new york times"}
        # self.my_dictionary = []
        # for new in self.data_new:
        #     #print(new)
        #     self.my_dictionary.append(self.cleanDoc(new["noticia"]))
        #     
        # self.dict_data = corpora.Dictionary(self.my_dictionary)
        # self.dict_data.save('dictionary.dict')
        # 
        # corpus = [self.dict_data.doc2bow(text) for text in self.my_dictionary]
        # corpora.MmCorpus.serialize('corporacorp.mm', corpus)
        #
        
        #self.pre_process_data()          
#        self.read_all_data_from_files()
#        self.process_query('christian',0,1420)
        

        # weightstf = [[wgt for word_id,wgt in doc] for doc in corpus_tfidf]
        # print(weightstf, end="\n")
        # 
        # for doc in corpus_tfidf:
        #     for (word_id, wgt) in doc:
        #         print(word_id, wgt),
        #     print("end of document"+'\n')
        # print('')
        # #pprint(self.dict_data.token2id)
        pass
    def pre_process_data(self):
        self.file_list = glob.glob('json_files/*.json')
        self.data_list = []
        for i_file in self.file_list:
            print(i_file)
            tmp_dictionary = self.json_obj.read_json_file(str(i_file))
            for i_dict in tmp_dictionary:
                try:                    
                    if self.json_obj.insert_data(i_dict['categoria'],i_dict['titulo'],i_dict['fecha'],i_dict['url']) == True: 
                        self.data_list.append(self.cleanDoc(i_dict['noticia']))
                    else:
                        print('new no accepted')
                        print('\n')
                        continue
                except KeyError:
                    if self.json_obj.insert_data(i_dict['Categoria'],i_dict['Titulo'],i_dict['Fecha'],i_dict['Url']) == True: 
                        self.data_list.append(self.cleanDoc(i_dict['Noticia']))
                    else:
                        print('new no accepted')
                        print('\n')
                        continue
                    
        print('end of reading and writing news database')
        
        self.data_dictionary = corpora.Dictionary(self.data_list)
        self.data_dictionary.save('path_preprocess/dictionary.dict')
        print('end dictionary preprocess')
        
        self.corpus = [self.data_dictionary.doc2bow(text) for text in self.data_list]
        corpora.MmCorpus.serialize('path_preprocess/corpora.mm',self.corpus)
        
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
        self.corpus_tfidf = self.tfidf[self.corpus]
        
        index = similarities.Similarity('path_preprocess/matrixSimilarities.txt',self.corpus_tfidf, num_features=len(self.data_list))
        #index = similarities.Similarity.load('matrixSimilarities.txt')
        index.save('path_preprocess/matrixSimilarities.txt')
        
    def read_all_data_from_files(self):
        self.dictionary = corpora.Dictionary.load('path_preprocess/dictionary.dict')
        self.corpus = corpora.MmCorpus('path_preprocess/corpora.mm')
        self.tfidf = models.TfidfModel(self.corpus, normalize=True)
        #self.corpus_tfidf = self.tfidf[self.corpus]
        self.index = similarities.Similarity.load('path_preprocess/matrixSimilarities.txt')

     
    def cleanDoc(self,doc):
        stopset = set(stopwords.words('spanish'))
        stemmer = nltk.PorterStemmer()
        tokens = WordPunctTokenizer().tokenize(doc)
        clean = [token.lower() for token in tokens if token.lower() not in stopset and len(token) > 2]
        final = [stemmer.stem(word) for word in clean]
        return final
    
    def process_query(self,query):
        self.my_query = query
        print(self.my_query)
        self.new_vec = self.dictionary.doc2bow(self.cleanDoc(self.my_query))
        print('end matrix')
        sims = self.index[self.tfidf[self.new_vec]]
        #print(list(enumerate(sims)))
        list_sims = []
        for similar in enumerate(sims):
            #print(type(similar))
            if similar[1] != 0:
                list_sims.append(similar)
        print(list_sims)
        list_sims = sorted(list_sims, key = lambda list_sims: list_sims[1],reverse = True)
        
        for i_sim in list_sims:
            print(i_sim)
        print('\n\n')
        print(self.new_vec)
        return list_sims
    
    def __iter__(self):
        for line in open('corpus.txt'):
            yield dictionary.doc2bow(line.lower().split())



proc_mnger = PreProcessManager()
proc_mnger.read_all_data_from_files()
proc_mnger.process_query("christian")