# FallGuysCharts Full Version History

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
- General: Added last new map, added Squads Mode and Slam Dunk playlist info, and fixed a mispelling in to fallGuysStructures.py; 
added getSquadDataFrames() to get Squad Mode shows; 
added a Normalized Position column to the rounds DataFrame returned by getDataFrames() and the one returned by getMapInfoDataFrame(); 
added getPlaylistTimeAndWins(), getSquadsFinalsDataFrame(), and getSquadRoundName(); 
added fallGuysStructures.py to the zip
- Graphs: added 8 new graph functions: normalizedPositionRaceBar(), seasonMapsQualPercentBar(), 
seasonPlaylistTimeBar(), seasonPlaylistWinsBar(), seasonPlaylistMinutesPerWinBar(), 
playsPerWinPlaylistBar(), squadsFinalWinPercentBar(), and squadsFinalStackedBar()
- Statistics: Added a season parameter to getPlaylistInfoDataFrame() and 
flexibility to handle squads playlists; added getSquadShowStats() to accurately 
get data for squads playlists

### 1.0.4 (3/23/2021)
- General: Added a new playlist dict, data for 6/7 new maps, and some other playlist info to fallGuysStructures.py
- Tracker: Missed renaming one variable, updated getSeason() for season 4 start time, and updated message after running fallGuysData.py

### 1.0.3 (3/21/2021)
- General: Removed 'Fall Guys Slim.ipynb', changed remaining variables that 
used the camelCase naming convention to use underscores instead, and added 
special shows to fallGuysStructures.py
- Graphs: Added a percent and an explode parameter for specialShowsPie

### 1.0.2 (3/20/2021)
- General: Added info for Thin Ice Trials rounds
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