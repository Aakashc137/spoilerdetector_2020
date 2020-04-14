#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import re
from pathlib import Path
home = str(Path.home())

def createdir(path):
    if os.path.isdir(path)==True:
        print("directory ",path," already exists.")
        return 1
    else:
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
            return 2
        else:
            print ("Successfully created the directory %s " % path)
            return 3
        
def createfile(path):
    if os.path.isfile(path)==True:
        print("file ",path," already exists.")
        return 1
    else:
        try:
            f = open(path,"w")
            f.close()
        except IOError:
            print ("Creation of the file %s failed" % path)
            return 2
        else:
            print ("Successfully created the file %s " % path)
            return 3
        
def write(path,mode,*args):
    if mode==1:
        f = open(path,"a")
        f.write(args[0])
        f.close()
    elif mode==2:
        f = open(path,"a")
        for character in args[0]:
            f.write(character)
            f.write("\n")
        f.close()
    elif mode==3:
        f = open(path,"a")
        f.write(args[0])
        f.write(",")
        f.write(args[1][0])
        f.write("\n")
        f.write(args[1][1])
        f.close()

def libcreate(moviename,synopsis,characters,review):
    cwd = str(Path.home())
    cwd=cwd+"/moviereviews"
    
    
    status=createdir(cwd)           #create dir
    if status==2:
        exit()
    parentdir=cwd
    
    
    hashtitle=str(hash(moviename))
    moviedir=cwd+"/"+hashtitle
    masterfile=cwd+"/"+"masterfile.txt"
    status=createdir(moviedir)      #create dir of a movie
    if status==2:
        exit()
    
    staus=createfile(masterfile)
    if status==2:
        exit()
    
    filename=moviedir+"/"+hashtitle+".txt"
    staus=createfile(filename)      #create file of movie using hashcode
    if status==2:
        exit()
    elif status==3:
        write(filename,1,moviename)
        f=open(masterfile,"a")
        f.write(hashtitle)
        f.write("\n")
        f.close()
        
    
    
    filename=moviedir+"/"+hashtitle+"_s"+".txt"
    staus=createfile(filename)      #create file of movie synopsis using hashcode
    if status==2:
        exit()
    elif status==3:
        write(filename,1,synopsis)
    
    
    filename=moviedir+"/"+hashtitle+"_c"+".txt"
    staus=createfile(filename)      #create file of movie character using hashcode
    if status==2:
        exit()
    elif status==3:
        write(filename,2,characters)
    
    
    count=0
    for x,y in review.items():
        count+=1
        filename=moviedir+"/"+hashtitle+"_"+str(count)+".txt"
        staus=createfile(filename)  #create file of review using movie name
        if status==2:
            exit()
        elif status==3:
            write(filename,3,x,y)         #y is a dictionary with first element as s/n and second element as a review


        
f1 = open("tafr10.json","r+")
m_title = {}
for i in f1:
    words = i.split('"')
    if(len(words))>1:
        rlist = []
        for j in range(len(words)):
            if(j>=7 and j%2!=0):
                rlist.append(words[j][0:-2])
        m_title.update({words[3]:rlist})
f1.close()

f2 = open("all_reviews.json","r+")
m_reviews = {}
for i in f2:
    words = i.split('"')
    count = 1
    review_dict = {}
    if len(words)>1:
        chunks = re.split("Permalink",i)
        chunks = chunks[0:-1]
        for schunks in chunks:
            reviews = schunks.split(r'"')
            if(len(reviews)>5):
                review_str = ""
                num = -17
                while(num>=-30 and len(reviews)>(-num)):
                    if(len(reviews[num]))>1:
                        if(len(reviews[num][0:-1])>30):
                            review_str = reviews[num][0:-1] + review_str
                    num = num - 1
                review_dict.update({("review{}".format(count)):review_str})
                count = count + 1
        m_reviews.update({words[3]:review_dict})
f2.close()
    
    
    
    
    
f2 = open("noSpoiler_reviews.json","r+")
noSpoiler_reviews = {}   
for i in f2:
    words = i.split('"')
    count = 1
    review_dict = {}
    if len(words)>1:
        chunks = re.split("Permalink",i)
        chunks = chunks[0:-1]
        for schunks in chunks:
            reviews = schunks.split(r'"')
            if(len(reviews)>5):
                review_str = ""
                num = -17
                while(num>=-30 and len(reviews)>(-num)):
                    if(len(reviews[num]))>1:
                        if(len(reviews[num][0:-1])>30):
                            review_str = reviews[num][0:-1] + review_str
                    num = num - 1
                review_dict.update({("review{}".format(count)):review_str})
                count = count + 1
        noSpoiler_reviews.update({words[3]:review_dict})
f2.close()
    
    
    
    
    
    
    
labelled_reviews = {}
mcount = 0
scount = 0
for i,j in m_reviews.items():
    scount=0
    review_dict = {}
    for mcount in range(len(m_reviews[i])):
        tl = []
        if "review{}".format(scount+1) in noSpoiler_reviews[i].keys():
            if(m_reviews[i]["review{}".format(mcount+1)])!=(noSpoiler_reviews[i]["review{}".format(scount+1)]):
                tl.append('S')
                tl.append(m_reviews[i]["review{}".format(mcount+1)])
            else:
                tl.append('N')
                tl.append(m_reviews[i]["review{}".format(mcount+1)])
                scount = scount + 1
            review_dict.update({"review{}".format(mcount+1):tl})
    labelled_reviews.update({i:review_dict})

    
    
f2 = open("fsynopsis.json","r+") 
synopsis_dict = {}
for i in f2:
    words = i.split('"')
    if(len(words)>1):
        if words[11] == "It looks like we don't have a Synopsis for this title yet. ":
            synopsis_dict.update({words[3]:"No Synopsis"})
        else:
            synopsis_string = ""
            for j in range(len(words)):
                if len(words[j])>5 and j>=9 :
                    synopsis_string = synopsis_string + words[j]
            synopsis_dict.update({words[3]:synopsis_string})



f2 = open("characterlist.json","r+") 
character_dict = {}
for i in f2:
    words = i.split('"')
    if(len(words)>1):
        il = []
        for j in range(len(words)):
            if j>=7 and j%2!=0:
                if not ("episode" in words[j]):
                    il.append(words[j])
        character_dict.update({words[3]:il})


        
reference_dict = {}
for i,j in synopsis_dict.items():
    if j != "No Synopsis":
        il = []
        if i in labelled_reviews.keys() and i in character_dict.keys():
            il.append(j)
            il.append(character_dict[i])
            il.append(labelled_reviews[i])
        reference_dict.update({i:il})

        
for moviename,sclr in reference_dict.items():
    libcreate(moviename,sclr[0],sclr[1],sclr[2])


# In[ ]:




