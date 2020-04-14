#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishvapatel 18bce260 aakashshah 18bce214 yashchelani 18bce263
"""
import nltk as n
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet
import pickle
import os

porter = PorterStemmer()
stopwords=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
VB_list=["VB","VBD","VBG","VBN","VBP","VBZ"]    
cwd=os.path.dirname(os.path.abspath(__file__))

def fetchtotal_set():

    f=open(os.path.join(cwd,"total_set.data"),"rb")
    tl=pickle.load(f)
    f.close()
    return tl

def fetchtest_set(): 
    f=open(os.path.join(cwd,"test_set.data"),"rb")
    tl=pickle.load(f)
    f.close()
    return tl
 
def updatetotal_set(update):
    f=open(os.path.join(cwd,"total_set.data"),"rb")
    tl=pickle.load(f)
    f.close()
    tl.append(update)

    f=open(os.path.join(cwd,"total_set.data"),"wb")
    pickle.dump(tl,f)
    f.close()
    print("total set updated")
    
def updatemachine(machine):
    f=open(os.path.join(cwd,"detector.data"),"wb")
    pickle.dump(machine,f)
    f.close()
    print("updated machine stored")
    
def fetchmachine():
    f=open(os.path.join(cwd,"detector.data"),"rb")
    machine=pickle.load(f)
    f.close()
    return machine
    
def trainmachine():
    total_set=fetchtotal_set()
    train_set=total_set
    return n.DecisionTreeClassifier.train(train_set)

def sentenceVerb_features(characters,pos_tagged_s,reviewSentence_list,verbsynonym_s):
    total_sentences = len(reviewSentence_list)
    tot_occ_char_verb = 0
    for i in reviewSentence_list:
        if(len(i)!=0):
            v_bool=False
            c_bool=False
            words = n.tokenize.word_tokenize(i)
            pos_tagged_r = n.pos_tag(words)
            pos_tagged_r=[(porter.stem(w),l) for w,l in pos_tagged_r if w not in stopwords and w.isalnum()]
            
            for x in words:
                if x in characters:
                    c_bool=True
                    break        
            for x,y in pos_tagged_r:
                if y in VB_list and x in verbsynonym_s:
                    v_bool=True
                    break
            if c_bool and v_bool:
                tot_occ_char_verb = tot_occ_char_verb + 1
    per_occ_char_verb = tot_occ_char_verb/total_sentences
    return({"percentage_of_occurrence_character_verb":per_occ_char_verb})
    
    

def char_feature(characters,reviewlist):
    tot_occ_char=0
    per_tot_occ_char=0
    #reviewlist=[w for w in reviewlist if (w not in stopwords and w.isalnum())]
    if len(reviewlist)!=0:
        for i in characters:
            tot_occ_char+=reviewlist.count(i)
        per_tot_occ_char=tot_occ_char/len(reviewlist)
    return ({"percentage_of_occurence_character":per_tot_occ_char})


def verb_feature(pos_tagged_s,reviewlist,verbsynonym_s):
    #print("in verb feature")
    pos_tagged_r=n.pos_tag(reviewlist)
    pos_tagged_r=[(porter.stem(w),l) for w,l in pos_tagged_r if (w not in stopwords and w.isalnum())]
    words_r=[w for w,l in pos_tagged_r]
    
    tot_occ_verb=0
    per_tot_occ_verb=0
    
    verblist_r=set([x for x,y in pos_tagged_r if y in VB_list])
    
    if len(words_r)!=0:
        for i in verblist_r:
            if i in verbsynonym_s:
                tot_occ_verb+=words_r.count(i)
        per_tot_occ_verb=tot_occ_verb/len(words_r)
    return ({"percentage_of_occurence_verb":per_tot_occ_verb})



def setbuiler(characters,movie_s,movie_r):
    synopsislist=n.tokenize.word_tokenize(movie_s)                 # pos tagging synopsis early to avoid it doing again and again
    pos_tagged_s=n.pos_tag(synopsislist)
    pos_tagged_s=[(porter.stem(w),l) for w,l in pos_tagged_s if (w not in stopwords and w.isalnum())]   
    
    
    verblist_s=[x for x,y in pos_tagged_s if y in VB_list]
    verbsynonym_s = set(verblist_s)
    for i in verblist_s:
        for j in wordnet.synsets(i):
            for k in j.lemmas():
                verbsynonym_s.add(k.name())
        
    reviewSentence_list=n.tokenize.sent_tokenize(movie_r)
    reviewlist=n.tokenize.word_tokenize(movie_r)
    
    characters=[j.lower() for j in characters]       #making every word to lower
    ctemp=[]
    templist=[]
    for a in characters:                                            # separating lastname firstname
        templist=n.tokenize.word_tokenize(a)
        ctemp.extend(templist)
    characters=ctemp

    tot_features_dic={}
    tot_features_dic.update(char_feature(characters,reviewlist))
    tot_features_dic.update(verb_feature(pos_tagged_s,reviewlist,verbsynonym_s))
    tot_features_dic.update(sentenceVerb_features(characters,pos_tagged_s,reviewSentence_list,verbsynonym_s))
    return tot_features_dic


def reviewpredictor(detector,characters,movie_s,movie_r):
    return detector.classify(setbuiler(characters,movie_s,movie_r))

def reviewfeeder(movie_c,movie_s,movie_r,sn):
    feature_dict=setbuiler(movie_c,movie_s,movie_r)
    updatetotal_set((feature_dict,sn))
    machine=trainmachine()
    updatemachine(machine)
    return machine
    
