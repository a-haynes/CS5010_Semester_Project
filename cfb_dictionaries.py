# Import libraries
import requests
from bs4 import BeautifulSoup

#Pulling Team Info from Wikipedia
page = requests.get('https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_FBS_football_programs')
# Create a BeautifulSoup object
soup = BeautifulSoup(page.text, 'html.parser')

# Pull all text from the table div
table = soup.find('table')
table_body = table.find('tbody')
rows = table_body.find_all('tr')

# Finding the nth occurance of a substring in a string, 
# Used for parsing through \n's in Wikipedia table
def find_nth(string, substring, n):
    start = string.find(substring)
    while start >= 0 and n > 1:
        start = string.find(substring, start+len(substring))
        n -= 1
    return start

nicknames = {} # Ex: Cavaliers
team_names = {} # Ex: Virginia Cavaliers
# Kaggle only contains Schools.
# ESPN has School + Nicknames (team_names) as single string.
# Pulling School and Nicknames into separate lists from Wikipedia
# makes linking the two easier, espcially in the case where one School name
# is contained in another, e.g. Virginia and Virginia Tech, and not erroneously
# parsing Virginia Tech : Hokies as Virginia : Tech Hokies


# Running through each row 
for team in rows[1:]: # Skip first row to avoid table headers
    school = team.get_text()[find_nth(team.get_text(),'\n', 1)+1:
                                find_nth(team.get_text(),'\n', 2)]
    nickname = team.get_text()[find_nth(team.get_text(),'\n', 3)+1:
                                find_nth(team.get_text(),'\n', 4)]
    nicknames[school] = nickname
    team_names[school+' '+nickname] = school
nicknames['Idaho']='Vandals' # Idaho Vandals dropped to FCS in 2017
team_names['Idaho Vandals'] = 'Idaho' # So they aren't in the table
    

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
            # Manually fixing some mismatched abbreviations
        if (team.get_text() == 'Miami Hurricanes') :
            logos['Miami (FL)'] = team_logo
        elif (team.get_text() == 'Southern Mississippi Golden Eagles'):
            logos['Southern Miss'] = team_logo
        elif (team.get_text() == 'UT San Antonio Roadrunners'):
            logos['UTSA'] = team_logo
        elif (team.get_text() == 'UL Monroe Warhawks'):
            logos['Louisiana–Monroe'] = team_logo
        elif (team.get_text() == 'Florida International Panthers'):
            logos['FIU'] = team_logo
        elif (team.get_text() == 'San José State Spartans'):
            logos['San Jose State'] = team_logo
        elif (team.get_text() == 'Hawai\'i Rainbow Warriors'):
            logos['Hawaii'] = team_logo
        else:
            logos[team_names[team.get_text()]] = team_logo
logos['Idaho'] = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
    + "70.png&h=50&w=50"
logos['New Mexico State'] = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
    + "166.png&h=50&w=50"
logos['UConn'] = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
    + "41.png&h=50&w=50"
logos['Old Dominion'] = "https://a.espncdn.com/combiner/i?img=/i/teamlogos/ncaa/500/"\
    + "295.png&h=50&w=50"
    
    