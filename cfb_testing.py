#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:46:09 2021

@author: sarahrodgers

Testing Web Scraper Results
"""

import unittest
from cfb_dictionaries import *
from cfb_dataframe import *

# testing that the web scraped information was pulled correctly from Wikipedia
class CFBWikipediaTestCase(unittest.TestCase): #must inherit from unittest.TestCase

    # Are all school names stored correctly as keys
    def test_1(self):
        self.assertEqual(len(nicknames.keys()), 131)
    
    # Are all mascot names stored correctly as values
    def test_2(self):
        self.assertEqual(len(nicknames.values()), 131)
        
    # Is the expected mascot associated with the correct school
    def test_3(self):
        self.assertEqual(nicknames["Penn State"], 'Nittany Lions')
        
    def test_4(self):
        self.assertEqual(nicknames["Virginia"], 'Cavaliers')
        
    def test_5(self):
        self.assertEqual(nicknames.get('Air Force'), 'Falcons')
        
    def test_6(self):
        self.assertEqual(nicknames.get('Syracuse'), 'Orange')
        
    # Check that there are no missing mascot values for schools with known mascots
    def test_7(self):
        self.assertFalse(nicknames['Ohio State'] == '', msg= "The Ohio State mascot is not missing")
    
    def test_8(self):
        self.assertFalse(nicknames['Michigan'] == '', msg= "The Michigan mascot is not missing")
   
# testing that the web scraped information was pulled correctly from ESPN
class CFBESPNTestCase(unittest.TestCase): #must inherit from unittest.TestCase
    
    # Are all school names stored correctly as keys
    def test_9(self):
        self.assertEqual(len(logos.keys()),  131)
    
    # Are all logos stored correctly as values
    def test_10(self):
        self.assertEqual(len(logos.values()),  131)
        
    # Is the expected logo id associated with the correct school
    def test_11(self):
        self.assertTrue('50' in logos['Penn State'])
        
    def test_12(self):
        self.assertTrue('333' in logos['Alabama'])
        
    # Check that there are no missing logo values for schools with known logos
    def test_13(self):
        self.assertFalse(logos['Auburn'] == '', msg= "The Auburn logo is not missing")
    
    def test_14(self):
        self.assertFalse(logos['Navy'] == '', msg= "The Navy logo is not missing")
        
# testing that the dataframe used for the visualizations outputs the expected statsitics
class CFBVisualizationTestCase(unittest.TestCase): #must inherit from unittest.TestCase
    
    # Is the highest offensive ranked team what is expected for various years?
    def test_15(self):
        # For 2020
        temp = df_cfb[df_cfb['Indicator Name'] == 'Off.Rank']
        temp = temp[temp['Year'] == 2020]
        temp['Value'] = temp['Value'].astype(str).astype(int)
        max_off_rank = temp.loc[temp['Value'].idxmin()]
        self.assertEqual(max_off_rank['School'],  'Kent State')
    
    # Is the highest offensive ranked team what is expected for various years?
    def test_16(self):
        # For 2013
        temp = df_cfb[df_cfb['Indicator Name'] == 'Off.Rank']
        temp = temp[temp['Year'] == 2013]
        temp['Value'] = temp['Value'].astype(str).astype(int)
        max_off_rank = temp.loc[temp['Value'].idxmin()]
        self.assertEqual(max_off_rank['School'],  'Baylor')
        
    # Is the conference filter working properly?
    def test_17(self):
        # For AAC
        aac_conf = df_cfb[df_cfb['Conference'] == 'AAC']
        aac_teams = np.array(['Cincinnati', 'Houston', 'Louisville', 'Memphis', 'Rutgers', 'SMU',
       'South Florida', 'Temple', 'UCF', 'UConn', 'East Carolina',
       'Tulane', 'Tulsa', 'Navy'])
        self.assertEqual(print(aac_conf['School'].unique()), print(aac_teams))
    
    # Is the conference filter working properly?
    def test_18(self):
        # For Big Ten
        big_ten_conf = df_cfb[df_cfb['Conference'] == 'Big Ten']
        big_ten_teams = np.array(['Illinois', 'Indiana', 'Iowa', 'Michigan', 'Michigan State',
       'Minnesota', 'Nebraska', 'Northwestern', 'Ohio State',
       'Penn State', 'Purdue', 'Wisconsin', 'Maryland', 'Rutgers'])
        self.assertEqual(print(big_ten_conf['School'].unique()), print(big_ten_teams))
    
    # Is the team with the highest win percentage team what is expected?
    def test_19(self):
        # For 2019
        temp = df_cfb[df_cfb['Indicator Name'] == 'WinPct']
        temp = temp[temp['Year'] == 2019]
        temp['Value'] = temp['Value'].astype(float)
        max_win_percentage = temp.loc[temp['Value'].idxmax()]
        self.assertEqual(max_win_percentage['School'],  'LSU')
    
    # Is the value of the team with the highest win percentage team what is expected?
    def test_20(self):
        # For 2020
        temp = df_cfb[df_cfb['Indicator Name'] == 'WinPct']
        temp = temp[temp['Year'] == 2020]
        temp['Value'] = temp['Value'].astype(float)
        max_win_percentage = temp.loc[temp['Value'].idxmax()]
        self.assertEqual(max_win_percentage['Value'],  1)

if __name__ == '__main__':
    log_file = 'CFB Testing.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)