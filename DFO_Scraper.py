#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:23:02 2018

@author: daviddevito
"""

# This script scrapes NHL rosters and stats for each team from dailyfaceoff.com
# It outputs the rosters and stats of each team into a separate text file

import requests
from bs4 import BeautifulSoup
import re

# Array of all team names
teamName = ["anaheim-ducks","arizona-coyotes","boston-bruins","buffalo-sabres","calgary-flames","carolina-hurricanes","chicago-blackhawks","colorado-avalanche","columbus-blue-jackets","dallas-stars","detroit-red-wings","edmonton-oilers","florida-panthers","los-angeles-kings","minnesota-wild","montreal-canadiens","nashville-predators","new-jersey-devils","new-york-islanders","new-york-rangers","ottawa-senators","philadelphia-flyers","pittsburgh-penguins","san-jose-sharks","st-louis-blues","tampa-bay-lightning","toronto-maple-leafs","vancouver-canucks","vegas-golden-knights","washington-capitals","winnipeg-jets"]

# Loop through each team
for k in range(0,len(teamName)):
    print(teamName[k])
    
    # Open text file named after team
    fileToOpen = teamName[k] + '.txt'
    fileName = open(fileToOpen,"w")
    # Printing headers
    fileName.write('Name\tGoals\tAssists\tShots\tBlocks\tPPP\tMin/Gm\tDKSalary\tFDSalary\tShots+Blocks/GM\tDKPts/GM\n')
    
    # Access team page on dailyfaceoff.com and scrape content
    url = "https://www.dailyfaceoff.com/teams/" + teamName[k] + "/line-combinations/stats/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    
    name_data = soup.find_all("a", {"class": "player-link"})
    stats_data = soup.find_all("div", {"class": "last-five-stats player-stat-wrap"})
    
    # Writing data to text file
    for i in range(0,28):
        # Write Forward line and DPair header
        header_lines = [0,3,6,9,12,14,16,18,23]
        if i == 18 or i == 23:
            fileName.write("\n")
        header_text = ['Line 1','Line 2','Line 3','Line 4','DPair 1','DPair 2','DPair 3','PP1','PP2']
        if i in header_lines:
            fileName.write(header_text[header_lines.index(i)] + "\n")
    
        # Get Player Name
        name = name_data[i].img["alt"]
    
        # Get Stats
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
        # Calculating Shots+Blocks per Game Last 5 Games
        x = (int(stats[2]) + int(stats[3]))/5
        outputStr = outputStr + str(x) + '\t'
        # Calculating DK/Pts per Game Last 5 Games
        y = ((float(stats[0])*3) + (float(stats[1])*2) + (float(stats[2])*0.5) + (float(stats[3])*0.5))/5
        outputStr = outputStr + str(y)
        # Write Line to Text File
        fileName.write(outputStr + "\n")