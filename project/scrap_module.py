#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:17:15 2020

@author: vishvapatel
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

def Scrape(url_raw):
    urllist = url_raw.split("/")
    urllist = urllist[0:-1]
    url = ""
    for i in urllist:
        url = url + i + "/"
    url_s = url+"synopsis"        #url for extracting synopsis and MovieTitle
    url_c = url+"fullcredits"     #url for extracting characters
    try:
        page = urlopen(url_c)
    except:
        print("Error opening the URL")
        return False


    soup = BeautifulSoup(page, 'html.parser')


    content = soup.find_all('td', {"class": "character"})

    characterlist = []
    for i in content:
        if(i.find('a')!=None):
            characterlist.append(i.find('a').text)
   #print(characterlist)
    print("\n")


    try:
        page = urlopen(url_s)
    except:
        print("Error opening the URL")


    soup = BeautifulSoup(page, 'html.parser')

    content = soup.find('ul', {"id": "plot-synopsis-content"})
    title = soup.find('div',{"class":"parent"})
    MovieTitle = title.find('a').text
    #rint(MovieTitle)
    synopsis = ''
    for i in content.findAll('li'):
        synopsis = synopsis + i.text

    #rint(synopsis)
    return (MovieTitle,characterlist,synopsis)