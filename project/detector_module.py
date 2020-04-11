#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:27:51 2020

@author: vishvapatel
"""
import nltk as n
from nltk.stem.porter import PorterStemmer
import pickle
import os
import sys

porter = PorterStemmer()
stopwords = n.corpus.stopwords.words('english')


def fetchtotal_set():
    print(sys.path[0])
    f=open(os.path.join(sys.path[0],"total_set.data"),"rb")
    tl=pickle.load(f)
    f.close()
    return tl
 
def updatetotal_set(update):
    f=open(os.path.join(sys.path[0],"total_set.data"),"rb")
    tl=pickle.load(f)
    f.close()
    tl.append(update)

    f=open(os.path.join(sys.path[0],"total_set.data"),"wb")
    pickle.dump(tl,f)
    f.close()
    print("total set updated")
    
    
def trainmachine():
    total_set=fetchtotal_set()
    tt=len(total_set)
    test_set=total_set[:int(0.15*tt)]
    train_set=total_set[int(0.15*tt)+1:]
    return n.NaiveBayesClassifier.train(train_set)

def sentenceVerb_features(characters,pos_tagged_s,reviewSentence_list):
    VB_list=["VB","VBD","VBG","VBN","VBP","VBZ"]
    verblist_s=[x for x,y in pos_tagged_s if y in VB_list]
    total_sentences = len(reviewSentence_list)
    tot_occ_char_verb = 0
    for i in reviewSentence_list:
        if(len(i)!=0):
            v_bool=False
            c_bool=False
            words = n.tokenize.word_tokenize(i)
            pos_tagged_r = n.pos_tag(words)
            pos_tagged_r=[(w,l) for w,l in pos_tagged_r if w not in stopwords and w.isalnum()]
            pos_tagged_r=[(porter.stem(w),l) for w,l in pos_tagged_r]
            for x in characters:
                x=x.lower()
                if x in words:
                    c_bool=True
                    break        
            for x,y in pos_tagged_r:
                if y in VB_list and x in verblist_s:
                    v_bool=True
                    break
            if c_bool and v_bool:
                tot_occ_char_verb = tot_occ_char_verb + 1
    per_occ_char_verb = tot_occ_char_verb/total_sentences
    return({"percentage_of_occurrence_character_verb":per_occ_char_verb})
    
    

def char_feature(characters,reviewlist):
    tot_occ_char=0
    per_tot_occ_char=0
    if len(reviewlist)!=0:
        for i in characters:
            i=i.lower()
            tot_occ_char+=reviewlist.count(i)
        per_tot_occ_char=tot_occ_char/len(reviewlist)
    return ({"percentage_of_occurence_character":per_tot_occ_char})


def verb_feature(pos_tagged_s,reviewlist):
    pos_tagged_r=n.pos_tag(reviewlist)
    pos_tagged_r=[(w,l) for w,l in pos_tagged_r if (w not in stopwords and w.isalnum())]
    pos_tagged_r=[(porter.stem(w),l) for w,l in pos_tagged_r]
    tot_occ_verb=0
    per_tot_occ_verb=0
    VB_list=["VB","VBD","VBG","VBN","VBP","VBZ"]
    verblist_s=[x for x,y in pos_tagged_s if y in VB_list]
    verblist_r=[x for x,y in pos_tagged_r if y in VB_list]
    if len(reviewlist)!=0:
        for i in verblist_r:
            if i in verblist_s:
                tot_occ_verb+=pos_tagged_r.count(i)
        per_tot_occ_verb=tot_occ_verb/len(pos_tagged_r)
    return ({"percentage_of_occurence_verb":per_tot_occ_verb})

def setbuiler(characters,movie_s,movie_r):
    synopsislist=n.word_tokenize(movie_s)                
    pos_tagged_s=n.pos_tag(synopsislist)
    pos_tagged_s=[(w,l) for w,l in pos_tagged_s if (w not in stopwords and w.isalnum())]
    pos_tagged_s=[(porter.stem(w),l) for w,l in pos_tagged_s]
        
    reviewSentence_list=n.tokenize.sent_tokenize(movie_r)
    reviewlist=n.tokenize.word_tokenize(movie_r)
    
    tot_features_dic={}
    tot_features_dic.update(char_feature(characters,reviewlist))
    tot_features_dic.update(verb_feature(pos_tagged_s,reviewlist))
    tot_features_dic.update(sentenceVerb_features(characters,pos_tagged_s,reviewSentence_list))
    return tot_features_dic


def reviewpredictor(detector,characters,movie_s,movie_r):
    return detector.classify(setbuiler(characters,movie_s,movie_r))

def reviewfeeder(movie_c,movie_s,movie_r,sn):
    feature_dict=setbuiler(movie_c,movie_s,movie_r)
    updatetotal_set(feature_dict,sn)
    return trainmachine
    