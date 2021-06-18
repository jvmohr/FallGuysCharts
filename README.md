# FallGuysCharts
Code to track data and create graphs based on said data for Fall Guys.  

The main purpose of this project is the charts section. The tracker portion 
is mostly something I threw together so I could scrape as much data as possible 
from my logs. While it isn't hard to use, it does require a little bit of setup. 

The aim is to allow the charts section to work with data from popular trackers, 
so that you could simply upload your data to a webpage and view visualizations there.  

Examples of what the charts look like now can be found in [Fall Guys Exploration.ipynb](https://github.com/jvmohr/FallGuysCharts/blob/main/Fall%20Guys%20Data%20Exploration.ipynb). 

## To Do
- Make the tracker easier to setup/use
- Make the charts section work with data from popular trackers
- Launch a notebook as a webpage that allows users to upload data and pick graphs to be displayed


## Requirements
Python 3
- Can be downloaded from python.org  

Python libraries: pandas, numpy, matplotlib
- They can be downloaded by running 'pip install pandas numpy matplotlib' from the terminal / command prompt (should be able to search on your computer to find it)
-- May need to use pip3 instead of pip - if you do, use python3 instead of python for the following steps


## How To Use

### Initial Setup
1. Download zip and unzip it. 
2. Run setup script
- Hit shift and right-click in the unzipped folder and click on 'Open PowerShell window here'.
- Type `python fgstSetup.py` in the terminal and wait for it to complete.


### To Collect Data
Run the data collection script in PowerShell after each session by running `python fallGuysData.py` 
- Can open PowerShell similarly to as you did in the last step

Note: 
If you forget to run the script for a session, run 'python fallGuysData.py Player-prev.log' 
before running 'python fallGuysData.py' for your new session. 
This runs the script for the session before the most recent one. 
(Only text files for the most recent two sessions are saved.)


## Version History
(full changelog in [versions.md](https://github.com/jvmohr/FallGuysCharts/blob/main/versions.md)

### 1.1.3
- General: Added map info for The Slimescraper and Button Bashers; show info for X-treme Fall Guys, Blow Up, Hex-a-4041 Trials, No Teams, and Slimescraper Time; small formatting changes in fallGuysStructures.py

### 1.1.2 (5/11/2021)
- General: Added info for Roll Call, Big Yeetus Tour, and Fall Ball Cup playlists 
- Tracker: Fixed a problem where the game must switch maps in loading phase (had been partly fixed before)
- Graphs: Added mapStatsOverTimeLine()
- Statistics: Added getTopTimes() to get top n times user took on a specific map

### 1.1.1 (4/14/2021)
- General: Added Fall Mountain to getSquadRoundName(), added info for Slime Climb Time and Slam Dunk, and gave getSeconds() the ability to handle if there was no microseconds
- Tracker: Added two new columns, Actual Num Qual with Finals and Timeout, the first of which keeps track of the number of players that qualify for all rounds, including finals, and the latter of which is a boolean column for whether the final ended in a timeout or not
- Graphs: Edited squadsFinalWinPercentBar() to return finals won ratio and added winsBySeasonPie()
- Statistics: Fixed a problem in getMapInfoDataFrame() that arose due to the new Timeout column

### 1.1.0 (4/1/2021)
- General: Added/changed info in fallGuysStructures.py and added the file to the zip; 
added several functions, mostly revolving around Squads Mode; 
introducted normalized position; 
- Graphs: added 8 new graph functions
- Statistics: Several small changes

### 1.0.4 (3/23/2021)
- General: Added info to fallGuysStructures.py
- Tracker: Missed renaming one variable, updated with season 4 start time, and updated message after running fallGuysData.py

### 1.0.3 (3/21/2021)
- General: Removed 'Fall Guys Slim.ipynb', changed remaining variables that 
used the camelCase naming convention to use underscores instead, and added 
info to fallGuysStructures.py
- Graphs: Added 2 parameters for specialShowsPie()

### 1.0.2 (3/20/2021)
- General: Added info for Thin Ice Trials rounds
- Graphs: Added 3 new graph functions
- Statistics: Added getStreaks()

### 1.0.1 (3/16/2021)
- Tracker: Changed some time zone code
- Charts: Fixed a path inconsistency issue
- Cleaned up some comments

### 1.0.0 (3/12/2021)
- Initial
- Tracker: Working as of 3/13/2021
- Charts: Starting point