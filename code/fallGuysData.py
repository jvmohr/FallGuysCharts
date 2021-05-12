import os, datetime, sys, time, json
import pandas as pd
from fallGuysFcns import *

if len(sys.argv) >= 2:
    log_path = sys.argv[1]
else:
    # get log path from file
    with open("log_path.txt") as f:
        log_path = f.read()

# gets time zone
HOURS_DIFFERENTIAL = getTZ()

with open('totalshows.txt') as f:
    total_shows = f.read()
total_shows = int(total_shows.strip())

with open(os.path.join('data', 'session.txt')) as f:
    session_num = f.read()
session_num = int(session_num)
    


with open(log_path) as f:
    lines = f.read()

lines = lines.split('\n')
#lines = preprocessGrade2(lines)
lines = preprocessGrade4(lines)
lines = preprocessGrade5(lines)

# get first line of each new show and usernames used for show
prev_user = '!!!!!!!!!!!!!!!'
look_user = True
in_round = False
in_a_round = False
num_players_lock = False
finished = False
undo_time = False
received = False
to_skip = False
game_mode = 'main_show'
party_size = 'na'

episode_markers = []
usernames = []
party_sizes = []

# times
reg = []
conne = []
start_round_lines = []
user_end_round_lines = []
actual_end_round_lines = []

poss_lines = []
game_modes = []
# to find the actual number of players that qualified (for racing rounds)
prev_num_line = "green"
num_lines = []

# checking for timeout (Jump Showdown)
succeeded = []

# **********************************************************
# go through lines, looking for certain things**************
# **********************************************************
for i, line in enumerate(lines):
    # for username
    if '[CATAPULT] Attempting login' in line:
        finished = False
        received = False
    if 'Received disconnect reason from Catapult:' in line:
        to_skip = True
    if look_user and 'Sending login request' in line:
        usernames.append(line.split(' player ')[-1].split(' networkID')[0].replace(',', ''))
        prev_user = usernames[-1]
        look_user = False   
    # for type of show (main or alternate) (also called playlist)
    elif 'Chosen Show:' in line: # appears before entering matchmaking solo/group (not as of start of s3)
        game_mode = line.split(':')[-1]
        
    # signifies start of looking for new episode
    # get size of party
    elif 'Party Size' in line or 'Begin matchmaking solo' in line:
        if 'Begin matchmaking solo' in line:
            party_size = 1
        else:
            party_size = int(line.split(' ')[-1].strip())
    # for show start time
    elif '[QosManager] Registered' in line or 'QosManager: Registered' in line or '[QosManager] Updated next periodic check' in line: # for registered time (date)
        to_add_reg = line
    elif "[StateConnectToGame] We're connected to the server!" in line: # for connection time
        to_add_conne = line
    # for playlist
    elif 'Selected show is' in line: # appears before every round as of s3
        game_mode = line.split('Selected show is')[-1]
    # for server ID and map lines
    elif 'Received NetworkGameOptions from ' in line: 
        tmp = line.split('roundID=')[-1]
        serverID = line.split(' ')[4]
        if 'Default' not in tmp:
            poss_lines.append([serverID, tmp, i, line.split(': ')[0]])
            
        received = True
    # for start round times and players that qualified from previous round
    elif 'state from Countdown to Playing' in line:
        start_round_lines.append(line.split(': [')[0])
        in_round = True
        in_a_round = True
        num_players_lock = False
        users_succeeded = 0
        # append last # players achieving obj when hit new round
        if prev_num_line != "green":
            num_lines.append(prev_num_line.split('=')[-1])
            prev_num_line = ""
    elif 'Changing state from GameOver to Results' in line: # occassionally a random NumPlayers... line right before new round
        num_players_lock = True
    elif '[ClientGameSession] NumPlayersAchievingObjective=' in line: # for total number of players that quality
        if not num_players_lock:
            prev_num_line = line
    # for end round / player active in round times
    elif '[ClientGameManager] Handling unspawn for player FallGuy' in line and prev_user in line:
        if in_round:
            user_end_round_lines.append(line.split(': [')[0])
            in_round = False
    elif 'Changing local player state to: SpectatingEliminated' in line: # no longer appears as of ` Nov 21, 2020
        if in_round:
            user_end_round_lines.append(line.split(': C')[0])
            in_round = False
    elif 'is succeeded=True' in line:
        users_succeeded += 1
    elif 'Changing state from Playing to GameOver' in line: # 'Changing state from GameOver to Results'
        if in_a_round:
            in_a_round = False
            actual_end_round_lines.append(line.split(': [')[0])
            succeeded.append(users_succeeded)
            users_succeeded = 0
    # overall show data
    elif '[CompletedEpisodeDto]' in line: # marker for a good show; only append show stats here
        if received == False: 
            continue
        if to_skip:
            to_skip = False
            continue
        if finished: # last one was for a disconnected show then
            # save disconnected game
            final_lines = getShowLines(lines, episode_markers[-1])
            show_data, rounds = roundSplit(final_lines)
            disc_json = {'session': session_num, 'show_data': show_data, 'rounds': rounds}
            with open(os.path.join('data', 'disconnected.json')) as json_file: 
                data = json.load(json_file)
            data.append(disc_json)
            with open(os.path.join('data', 'disconnected.json'), 'w') as f: 
                json.dump(data, f) 
            
            party_sizes[-1] = party_size
            game_modes[-1] = game_mode
            episode_markers[-1] = i
            reg[-1] = to_add_reg
            conne[-1] = to_add_conne
            if undo_time:
                actual_end_round_lines = actual_end_round_lines[::-1]
                actual_end_round_lines.remove('left')
                actual_end_round_lines = actual_end_round_lines[::-1]
                undo_time = False
            if in_a_round:
                actual_end_round_lines.append('left')
                in_a_round = False
                undo_time = True
                succeeded.append(users_succeeded)
            look_user = True
            finished = True
            continue
        
        party_sizes.append(party_size)
        game_modes.append(game_mode)
        episode_markers.append(i)
        reg.append(to_add_reg)
        conne.append(to_add_conne)
        look_user = True
        party_size = 'na'
        finished = True
        if in_a_round:
            actual_end_round_lines.append('left')
            in_a_round = False
            undo_time = True
            succeeded.append(users_succeeded)
# end for

# append last # achieving obj
num_lines.append(prev_num_line.split('=')[-1])

# if no episodes found, end
if len(episode_markers) == 0:
    print('no episodes found') # change
        
# **********************************************************        
# get time user spent in each round ************************        
# (time round starts until they either finish or are eliminated) (just qualify I think)
# **********************************************************
# gets round times: user's time in round and total round time
round_times, actual_round_times = getRoundTimes(start_round_lines, user_end_round_lines, actual_end_round_lines)

# gets start times for each show
start_times = getStartTimes(reg, conne, HOURS_DIFFERENTIAL)


# **********************************************************
# for each show/episode ************************************
# **********************************************************
round_idx = 0
shows_saved = 0
shows_skipped = 0
saved_a_show = False

rnds = getExtraRoundInfoLines(poss_lines)
    
for show_idx, (j, user) in enumerate(zip(episode_markers, usernames)):
    this_show = total_shows
    total_shows += 1
    
    # get lines for this show
    final_lines = getShowLines(lines, j)
    
    # split data
    show_data, rounds = roundSplit(final_lines)
    
    # set show data
    show_dict = {}
    show_dict['Show ID'] = this_show # id
    show_dict['Start Time'] = start_times[show_idx]
    show_dict['Season'] = getSeason(start_times[show_idx], HOURS_DIFFERENTIAL) 
    show_dict['Time Taken'] = getTimeTaken(start_times[show_idx], final_lines[0].split(': ==')[0], HOURS_DIFFERENTIAL) # approximate time taken
    show_dict['Game Mode'] = game_modes[show_idx]
    show_dict['Final'] = False
    show_dict['Rounds'] = len(rounds) # num rounds
    show_dict['Username'] = user
    show_dict['Party Size'] = party_sizes[show_idx]
    show_dict['addID'] = final_lines[0].split(': ==')[0] # end time
    
    # add other show data
    for line in show_data:
        show_dict[line.split(':')[0]] = line.split(':')[1].strip()
    
    # ********************************************
    # get data for each round in show ************
    # ********************************************
    rounds_list = []
    # for each round in the show/episode
    for round_ in rounds: # for list in 2D list
        round_dict = {'Show ID': this_show, 
                      'Round Num': round_[0].split(' ')[1].strip(), 
                      'Map': round_[0].split('|')[1].strip()}
        round_dict['Time Spent'] = round_times[round_idx]
        round_dict['Round Length'] = actual_round_times[round_idx]
        
        # add rest of data from list
        for line in round_[1:]:
            round_dict[line.split(':')[0]] = line.split(':')[1].strip()
        
        # add extra information
        rnd = rnds[round_idx]
        splts = rnd.split()
        # round_dict['Participants'] = splts[5].split('=')[-1] # num people
        # round_dict['Qualification Percent'] = splts[8].split('=')[-1].replace(',', '') # qual %
        for x in splts:
            if 'currentParticipantCount' in x:
                round_dict['Participants'] = x.split('=')[-1]
            if 'qualificationPercentage' in x:
                round_dict['Qualification Percent'] = x.split('=')[-1].replace(',', '')
            if 'isFinalRound' in x:
                if x.split('=')[-1].replace(',', '') == 'True':
                    show_dict['Final'] = True
        round_dict['Actual Num Qual'] = num_lines[round_idx]
        round_dict['Actual Num Qual with Finals'] = succeeded[round_idx] # same as above but also keeps track of finals
        round_dict['Timeout'] = True if succeeded[round_idx] > 1 and show_dict['Final'] else False
        
        
        round_idx += 1
        rounds_list.append(round_dict)
    
    # ********************************************
    # save ***************************************
    # ******************************************** 
    # save show_dict to one csv
    # save each dict in rounds_list to another csv
    if not saveData(show_dict, rounds_list):
        shows_skipped += 1
        total_shows -= 1
    else:
        shows_saved += 1
        saved_a_show = True
# end for

if shows_skipped > 0:
    print('{}: csvs saved successfully with {} new shows while skipping {} shows that were already saved'.format(
        datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p'), shows_saved, shows_skipped))
else:
    print('{}: csvs saved successfully with {} new shows'.format(
        datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p'), shows_saved))

with open('totalshows.txt', 'w') as f:
    f.write(str(total_shows))

# save processed lines
if saved_a_show:
    with open(os.path.join('data', 'archive', 'session{}.txt'.format(session_num)), 'w') as f:
        f.write("\n".join(lines))
    session_num += 1

    with open(os.path.join('data', 'session.txt'), 'w') as f:
        f.write(str(session_num))
else:
    print('no new shows, not a new session')
