# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:52:14 2021

@author: rbc6wr
"""

# Import libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

dataset_url = 'https://raw.githubusercontent.com/a-haynes/CS5010_Semester_Project/main/datasets/cfb'

#Reading in the datasets
df_2013 = pd.read_csv(dataset_url + '13.csv')
df_2013.insert(1,'Year',2013)
df_2014 = pd.read_csv(dataset_url + '14.csv')
df_2014['Year'] = 2014
df_2015 = pd.read_csv(dataset_url + '15.csv')
df_2015['Year'] = 2015
df_2016 = pd.read_csv(dataset_url + '16.csv')
df_2016['Year'] = 2016
df_2017 = pd.read_csv(dataset_url + '17.csv')
df_2017['Year'] = 2017
df_2018 = pd.read_csv(dataset_url + '18.csv')
df_2018['Year'] = 2018
df_2019 = pd.read_csv(dataset_url + '19.csv')
df_2019['Year'] = 2019
df_2020 = pd.read_csv(dataset_url + '20.csv')
df_2020['Year'] = 2020

#Merging datasets into one dataframe
frames = [df_2013, df_2014, df_2015, df_2016, df_2017, df_2017, df_2018, df_2019,
          df_2020]
df_stats = pd.concat(frames)
df_stats = df_stats.dropna(axis=1)

df_stats['WinPct']=df_stats.Win / df_stats.Games

df_stats.Team = df_stats.Team.apply(lambda x: x.replace('St.', 'State'))
df_stats.Team=df_stats.Team.replace({"App State (Sun Belt)":"Appalachian State (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Fla. Atlantic (C-USA)":"Florida Atlantic (C-USA)"})
df_stats.Team=df_stats.Team.replace({"Ga. Southern (Sun Belt)":"Georgia Southern (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Massachusettes (FBS Independent)":"UMass (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"Western Ky. (C-USA)":"Western Kentucky (C-USA)"})
df_stats.Team=df_stats.Team.replace({"Western Mich. (MAC)":"Western Michigan (MAC)"})
df_stats.Team=df_stats.Team.replace({"Southern California (Pac-12)":"USC (Pac-12)"})
df_stats.Team=df_stats.Team.replace({"Connecticut (FBS Independent)":"UConn (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"ULM (Sun Belt)":"Louisiana–Monroe (Sun Belt)"})
df_stats.Team=df_stats.Team.replace({"Army West Point (FBS Independent)":"Army (FBS Independent)"})
df_stats.Team=df_stats.Team.replace({"Northern Ill. (MAC)":"Norther Illinois (MAC)"})
df_stats.Team=df_stats.Team.replace({"Southern Miss. (C-USA)":"Southern Miss (C-USA)"})

#Pulling Team Info from Wikipedia
page = requests.get('https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs')
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the table div
table = soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')

# Finding the nth occurance of a substring in a string
def find_nth(string, substring, n):
    start = string.find(substring)
    while start >= 0 and n > 1:
        start = string.find(substring, start+len(substring))
        n -= 1
    return start

schools = {}
nicknames = {}
conferences = {}
team_names = {}

for team in rows[1:]:
    school = team.get_text()[find_nth(team.get_text(),'\n', 1)+1:
                                find_nth(team.get_text(),'\n', 2)]
    nickname = team.get_text()[find_nth(team.get_text(),'\n', 3)+1:
                                find_nth(team.get_text(),'\n', 4)]
    conference = team.get_text()[find_nth(team.get_text(),'\n', 11)+1:
                                find_nth(team.get_text(),'\n', 12)]
    if conference == 'Independent' :
        conference = 'FBS Independent'
    key = school + ' (' + conference + ')'
    schools[key] = school
    nicknames[key] = nickname
    conferences[key] = conference
    team_names[schools[key] + ' ' + nicknames[key]] = key
    

# Collect ESPN's FPI Page (Page containing links to all FBS teams)
page = requests.get('https://www.espn.com/college-football/fpi/_/season/2020')

# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the Table__TBODY div
team_table = soup.find(class_='Table__TBODY')

# Pull text from all instances of data-clubhouse-uid attribute
# within Table__TBODY div
all_team_items = team_table.find_all(attrs={"data-clubhouse-uid": True}) 

logos = {}

# Loop through the all_team_items element and get the logo links
for team in all_team_items:
        team_id = team['data-clubhouse-uid'].partition('t:')[2]
        team_logo = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
            + team_id + ".png&h=50&w=50"
        if (team.get_text() == 'Miami Hurricanes') :
            logos['Miami (FL) Hurricanes'] = team_logo
        elif (team.get_text() == 'Southern Mississippi Golden Eagles'):
            logos['Southern Miss Golden Eagles'] = team_logo
        elif (team.get_text() == 'UT San Antonio Roadrunners'):
            logos['UTSA Roadrunners'] = team_logo
        elif (team.get_text() == 'UL Monroe Warhawks'):
            logos['Louisiana–Monroe Warhawks'] = team_logo
        elif (team.get_text() == 'Florida International Panthers'):
            logos['FIU Golden Panthers'] = team_logo
        elif (team.get_text() == 'San José State Spartans'):
            logos['San Jose State Spartans'] = team_logo
        elif (team.get_text() == 'Hawai\'i Rainbow Warriors'):
            logos['Hawaii Rainbow Warriors'] = team_logo
        else:
            logos[team_names[team.get_text()]] = team_logo


indicators = []
for col in df_stats.columns:
    if col not in ['Year', 'Team'] :
        indicators.append(col)
identifiers = ['Year', 'Team', 'School', 'Nickname', 'Conference', 'Logo']       

df_stats.insert(1,'School',df_stats['Team'].map(schools))
df_stats.insert(1,'Nickname',df_stats['Team'].map(nicknames))
df_stats.insert(1,'Conference',df_stats['Team'].map(conferences))
df_stats['Logo'] = df_stats['Team'].map(logos)
df_stats = df_stats.dropna()

df_stats = df_stats.melt(id_vars=identifiers, value_vars=indicators)

df_stats = df_stats.rename(columns={"variable": "Indicator Name"})