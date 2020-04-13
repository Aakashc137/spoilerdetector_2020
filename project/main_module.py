#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: vishvapatel 18bce260 aakashshah 18bce214 yashchelani 18bce263
"""
from scrap_module import Scrape
from detector_module import reviewfeeder,reviewpredictor,fetchmachine
from stat_module import plotgraph

def main(detector):
    while True:
        choice1=int(input("""enter one of the option 
                     \n1. USE THE SPOILER DETECTOR 
                     \n2. SHOW THE STATISTICAL DATA OF THE DETECTOR
                     \n0. EXIT""" ))
        if choice1==1:
            while True:
                choice2=int(input("""enter one of the option 
                         \n1. USE THE SPOILER DETECTOR TO PREDICT A REVIEW
                         \n2. USE THE SPOILER DETECTOR TO FEED A REVIEW
                         \n0. EXIT""" ))
                if choice2==1:
                    url=input("ENTER THE LINK OF THE MOVIE(IMDB) :")
                    info = Scrape(url)
                    if info!=False and len(info[0])!=0 and len(info[1])!=0 and len(info[2])!=0:
                        movie_t,movie_c,movie_s = info
                        movie_r = input("ENTER THE REVIEW OF THE MOVIE:")
                        reviewprediction=reviewpredictor(detector,movie_c,movie_s,movie_r)
                        if reviewprediction=="S":
                            print("THE DETECTOR PREDICTS THAT THE GIVEN REVIEW IS : SPOILER")
                        else:
                            print("THE DETECTOR PREDICTS THAT THE GIVEN REVIEW IS : NOT A SPOILER")
                    else:
                        print("could not fetch the information correctly")
                        exit()
                elif choice2==2:
                    url=input("ENTER THE LINK OF THE MOVIE(IMDB) :")
                    info = Scrape(url)
                    if info!=False:
                        movie_t,movie_c,movie_s = info
                        movie_r = input("ENTER THE REVIEW OF THE MOVIE:")
                        while True:
                            sn=input("""ENTER S IF THE REVIEW IS A SPOILER\nENTER N IF THE REVIEW IS NOT A SPOILER""").upper()
                            if sn in ["N","S"]:
                                break
                            else:
                                print("invlaid enter again...")
                        print("updating the total set and retaraining the detector ....")
                        detector=reviewfeeder(movie_c,movie_s,movie_r,sn)
                    else:
                        exit()
                elif choice2==0:
                    plotgraph()
                else:
                    print("enter a valid option...")
        elif choice1==2:
           print("work in progress")  
        elif choice1==0:
            break
        else:
            print("enter a valid option...")


if __name__ == "__main__":
    detector=fetchmachine()
    main(detector)
    

