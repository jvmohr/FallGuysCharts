# FallGuysCharts
Code to track data and create graphs based on said data for Fall Guys

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
### 1.0.1
- Tracker: Changed some time zone code
- Charts: Fixed a path inconsistency issue
- Cleaned up some comments

### 1.0.0
- Initial
- Tracker: Working as of 3/13/2021
- Charts: Starting point