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
### 1.0.2 (3/20/2021)
- General: Added info for Thin Ice Trials rounds and removed 'Fall Guys Slim.ipynb'
- Graphs: Added minutesPerWinBar(), winsBySeasonBar(), and specialShowsPie()
- Statistics: Added getStreaks()

### 1.0.1
- Tracker: Changed some time zone code
- Charts: Fixed a path inconsistency issue
- Cleaned up some comments

### 1.0.0
- Initial
- Tracker: Working as of 3/13/2021
- Charts: Starting point