#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishvapatel 18bce260 aakashshah 18bce214 yashchelani 18bce263
"""

import numpy as np
import matplotlib.pyplot as plt
from detector_module import fetchtest_set,fetchmachine,fetchtotal_set


def statistical_analysis_test_set():
    t_set=fetchtest_set()
    detector=fetchmachine()
    totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives=(0,0,0,0,0,0)
    for x,y in t_set:
        t2=detector.classify(x)
        if y=="S":
            totalPositives+=1
            if t2=="S":
                truePositives+=1
            else:
                falsePositives+=1
        if y=="N":
            totalNegatives+=1
            if t2=="N":
                trueNegatives+=1
            else:
                falseNegatives+=1
    return totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives
    

def statistical_analysis_total_set():
    t_set=fetchtotal_set()
    detector=fetchmachine()
    totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives=(0,0,0,0,0,0)
    for x,y in t_set:
        t2=detector.classify(x)
        if y=="S":
            totalPositives+=1
            if t2=="S":
                truePositives+=1
            else:
                falsePositives+=1
        if y=="N":
            totalNegatives+=1
            if t2=="N":
                trueNegatives+=1
            else:
                falseNegatives+=1
    return totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives   
 
def plotgraph():
    plt.rcParams['axes.facecolor'] = '#ffb308'
    totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives=statistical_analysis_test_set()
    data = [[totalPositives,totalNegatives],
    [truePositives,trueNegatives],
    [falsePositives,falseNegatives]]
    
    labels = ["Spoiler","NotSpoiler"]
    
    X = np.arange(2)
    
    
    plt.xticks([r + 0.15 for r in range(2)],labels)
    plt.ylabel("Reviews in numbers")
    
    bar1 = plt.bar(X + 0.00, data[0], color = '#000000', width = 0.15,label = "Total")
    bar2 = plt.bar(X + 0.15, data[1], color = 'g', width = 0.15,label = "Correct Classifications")
    bar3 = plt.bar(X + 0.30, data[2], color = 'r', width = 0.15,label = "False Classifications")
    
    for rect in bar1 + bar2 + bar3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center',va='bottom')
    
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    plt.rcParams['axes.facecolor'] = '#ffb308'
    totalPositives,truePositives,falsePositives,totalNegatives,trueNegatives,falseNegatives=statistical_analysis_total_set()
    data = [[totalPositives,totalNegatives],
    [truePositives,trueNegatives],
    [falsePositives,falseNegatives]]
    
    labels = ["Spoiler","NotSpoiler"]
    
    X = np.arange(2)
    
    
    plt.xticks([r + 0.15 for r in range(2)],labels)
    plt.ylabel("Reviews in numbers")
    
    bar1 = plt.bar(X + 0.00, data[0], color = '#000000', width = 0.15,label = "Total")
    bar2 = plt.bar(X + 0.15, data[1], color = 'g', width = 0.15,label = "Correct Classifications")
    bar3 = plt.bar(X + 0.30, data[2], color = 'r', width = 0.15,label = "False Classifications")
    
    for rect in bar1 + bar2 + bar3:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2.0, height, '%d' % int(height), ha='center',va='bottom')
    
    plt.legend()
    plt.tight_layout()
    plt.show()
