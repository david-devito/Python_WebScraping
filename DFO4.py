#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:23:02 2018

@author: daviddevito
"""

import requests
from bs4 import BeautifulSoup
import re

teamName = ["anaheim-ducks","arizona-coyotes","boston-bruins","buffalo-sabres","calgary-flames","carolina-hurricanes","chicago-blackhawks","colorado-avalanche","columbus-blue-jackets","dallas-stars","detroit-red-wings","edmonton-oilers","florida-panthers","los-angeles-kings","minnesota-wild","montreal-canadiens","nashville-predators","new-jersey-devils","new-york-islanders","new-york-rangers","ottawa-senators","philadelphia-flyers","pittsburgh-penguins","san-jose-sharks","st-louis-blues","tampa-bay-lightning","toronto-maple-leafs","vancouver-canucks","vegas-golden-knights","washington-capitals","winnipeg-jets"]
#teamName = input("Enter the team to run: ")
for k in range(0,len(teamName)):
    print(teamName[k])
    fileToOpen = teamName[k] + '.txt'
    
    fileName = open(fileToOpen,"w")
    #printing headers
    fileName.write('Name\tGoals\tAssists\tShots\tBlocks\tPPP\tMin/Gm\tDKSalary\tFDSalary\tShots+Blocks/GM\tDKPts/GM\n')
    
    url = "https://www.dailyfaceoff.com/teams/" + teamName[k] + "/line-combinations/stats/"
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content)
    
    name_data = soup.find_all("a", {"class": "player-link"})
    stats_data = soup.find_all("div", {"class": "last-five-stats player-stat-wrap"})
    
    for i in range(0,28):
        if i == 0: fileName.write('Line 1' + "\n")
        if i == 3: fileName.write('Line 2' + "\n")
        if i == 6: fileName.write('Line 3' + "\n")
        if i == 9: fileName.write('Line 4' + "\n")
        if i == 12: fileName.write('DPair 1' + "\n")
        if i == 14: fileName.write('DPair 2' + "\n")
        if i == 16: fileName.write('DPair 3' + "\n")
        if i == 18: fileName.write("\n" + 'PP1' + "\n")
        if i == 23: fileName.write("\n" + 'PP2' + "\n")
    
        name = name_data[i].img["alt"]
    
        stats_data[i] = str(stats_data[i])
        stats = re.findall(r'[0-9]+', stats_data[i])
        outputStr = str(name) + '\t'
        for k in range(0,len(stats)):
            if k <= 4 or k == 12 or k == 18:
                outputStr = outputStr + str(stats[k]) + '\t'
            if k == 5:
                if int(stats[5]) < 1000:
                    outputStr = outputStr + str(stats[5]) + '.' + str(stats[6]) + '\t'
                else:
                    outputStr = outputStr + '\t' + str(stats[5]) + '\t' + str(stats[6]) + '\t'
        #Calculating Shots+Blocks per Game Last 5 Games
        x = (int(stats[2]) + int(stats[3]))/5
        outputStr = outputStr + str(x) + '\t'
        #Calculating DK/Pts per Game Last 5 Games
        y = ((float(stats[0])*3) + (float(stats[1])*2) + (float(stats[2])*0.5) + (float(stats[3])*0.5))/5
        outputStr = outputStr + str(y)
        fileName.write(outputStr + "\n")