#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 10:49:53 2019

@author: daviddevito
"""

# This code scrapes Daily Baseball Lineups off of Rotogrinders.com
# It outputs all lineups and opposing pitchers into a text file

import requests
from bs4 import BeautifulSoup
import re

fileToOpen = 'MLBLineups.txt'
    
fileName = open(fileToOpen,"w")

url = "https://rotogrinders.com/lineups/mlb?site=draftkings"
    
r = requests.get(url)
    
soup = BeautifulSoup(r.content)

name_data = soup.find_all("div", {"class": "info"})

pitcher_name_data = soup.find_all("div", {"class": "pitcher players"})

pitcher_array = []
for k in range(0,(len(pitcher_name_data))):
    try:
        pitcher_array.append(pitcher_name_data[k].a.text)
    except:
        print("missing pitcher")

for i in range(0,270):
    player_name = name_data[i].a["title"]
    pos = name_data[i].find('span',class_='position').text
    pos = " ".join(pos.split())
    hand = name_data[i].find('span',class_='stats').text
    
    oppP = int(i/9)
    if oppP % 2 == 0:
        oppPAdjusted = oppP + 1
    else:
        oppPAdjusted = oppP - 1
    
    fileName.write(player_name + "\t" + pos + "\t" + pitcher_array[oppPAdjusted] + "\n")
