# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 14:52:14 2021

@author: rbc6wr
"""

# Import libraries
import pandas as pd

from cfb_dictionaries import logos, nicknames

dataset_url = 'https://raw.githubusercontent.com/a-haynes/CS5010_Semester_Project/main/datasets/cfb'

def make_df_cfb(year):
    df_year = pd.read_csv(dataset_url + str(year)[-2:] + '.csv')
    df_year['Year'] = year
    df_year['WinPct']=df_year.Win / df_year.Games
    df_year.Team=df_year.Team.replace({"App State (Sun Belt)":"Appalachian State (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Fla. Atlantic (C-USA)":"Florida Atlantic (C-USA)"})
    df_year.Team=df_year.Team.replace({"Ga. Southern (Sun Belt)":"Georgia Southern (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Massachusetts (FBS Independent)":"UMass (FBS Independent)"})
    df_year.Team=df_year.Team.replace({"Western Ky. (C-USA)":"Western Kentucky (C-USA)"})
    df_year.Team=df_year.Team.replace({"Western Ky. (Sun Belt)":"Western Kentucky (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Coastal Caro. (Sun Belt)":"Coastal Carolina (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Western Mich. (MAC)":"Western Michigan (MAC)"})
    df_year.Team=df_year.Team.replace({"Southern California (Pac-12)":"USC (Pac-12)"})
    df_year.Team=df_year.Team.replace({"Connecticut (FBS Independent)":"UConn (FBS Independent)"})
    df_year.Team=df_year.Team.replace({"ULM (Sun Belt)":"Louisiana–Monroe (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Army West Point (FBS Independent)":"Army (FBS Independent)"})
    df_year.Team=df_year.Team.replace({"Northern Ill. (MAC)":"Northern Illinois (MAC)"})
    df_year.Team=df_year.Team.replace({"Southern Miss. (C-USA)":"Southern Miss (C-USA)"})
    df_year.Team=df_year.Team.replace({"Central Mich. (MAC)":"Central Michigan (MAC)"})
    df_year.Team=df_year.Team.replace({"Eastern Mich. (MAC)":"Eastern Michigan (MAC)"})
    df_year.Team=df_year.Team.replace({"La.-Monroe (Sun Belt)":"Louisiana–Monroe (Sun Belt)"})
    df_year.Team=df_year.Team.replace({"Massachusetts (MAC)":"UMass (MAC)"})
    df_year.Team=df_year.Team.replace({"Middle Tenn. (C-USA)":"Middle Tennessee (C-USA)"})
    df_year.Team=df_year.Team.replace({"New Mexico State (FBS Independent)":"Middle Tennessee (C-USA)"})
    df_year.Team=df_year.Team.replace({"South Fla. (AAC)":"South Florida (AAC)"})
    df_year.Team=df_year.Team.replace({"Miami (FL) (ACC)":"Miami -FL- (ACC)","Miami (OH) (MAC)":"Miami -OH- (MAC)"})
    df_team=pd.DataFrame(df_year.Team.str.split("(",1).tolist(), columns = ['School','Conference'])
    df_conf=pd.DataFrame(df_team.Conference.str.split(")",1).tolist(), columns = ['Conference','x'])
    df_year['School'] = df_team.School.str.strip()
    df_year.School=df_year.School.replace({"Miami -FL-":"Miami (FL)","Miami -OH-":"Miami (OH)"})
    df_year['Conference'] = df_conf.Conference
    df_year.Conference = df_year.Conference.replace({'':"SEC"}) # Ole Miss has missing value
    df_year.School = df_year.School.apply(lambda x: x.replace('St.', 'State'))
    return df_year

#Reading in the datasets
df_2013 = make_df_cfb(2013)
df_2014 = make_df_cfb(2014)
df_2015 = make_df_cfb(2015)
df_2016 = make_df_cfb(2016)
df_2017 = make_df_cfb(2017)
df_2018 = make_df_cfb(2018)
df_2019 = make_df_cfb(2019)
df_2020 = make_df_cfb(2020)


#Merging datasets into one dataframe
frames = [df_2013, df_2014, df_2015, df_2016, df_2017, df_2017, df_2018, df_2019,
          df_2020]
df_cfb = pd.concat(frames)
df_cfb2 = df_cfb

indicators = []
for col in df_cfb.columns:
    if col not in ['Year', 'Team', 'School', 'Conference'] :
        indicators.append(col)
identifiers = ['Year', 'School', 'Nickname', 'Conference', 'Logo'] 

df_cfb['Logo'] = df_cfb.School.map(logos)
df_cfb['Nickname'] = df_cfb.School.map(nicknames)
df_cfb = df_cfb.melt(id_vars=identifiers, value_vars=indicators)
df_cfb = df_cfb.rename(columns={"variable": "Indicator Name","value": "Value"})
df_cfb = df_cfb.dropna()