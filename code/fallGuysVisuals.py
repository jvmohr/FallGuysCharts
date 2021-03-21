from fallGuysStructures import *
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import numpy as np

plt.rcParams['font.size'] = 14


# pie chart for a certain map - bonus tier
def mapBonusTiersPie(rounds_df, pick_map, eliminated=True, percent=False):
    try:
        for key in rounds_info_dict.keys():
            if rounds_info_dict[key]['Name'] == pick_map:
                pick_map = key
        pm_df = rounds_df[ rounds_df['Map'] == pick_map ]
    except:
        print("Couldn't find map....exiting.")
        return
    
    plays = len(pm_df)
    missed = len(pm_df[pm_df['Qualified'] == False])
    pm_df = pm_df[ pm_df['Qualified']]

    vc = pm_df['BadgeId'].fillna('none').value_counts()
    
    if missed != 0 and eliminated:
        vc['eliminated'] = missed
    else:
        plays -= missed

    pos_colors = ['gold', 'slategray', 'peru', 'blueviolet' , 'firebrick']
    pos_tiers = ['gold', 'silver', 'bronze',  'none', 'eliminated']
    colors = []
    tiers = []

    # eliminate sections that don't have positive values
    for tier, color in zip(pos_tiers, pos_colors):
        if tier in vc.index:
            colors.append(color)
            tiers.append(tier)

    vc = vc.reindex(index=tiers) # order it

    # plot it
    if percent:
        lbl_fcn = lambda x: "{:.2f}%".format(x)
    else:
        lbl_fcn = lambda x: int(round(plays * x / 100))
        
    plt.rcParams['font.size'] = 14
    plt.subplots(figsize=(7,7))
    plt.pie(vc, 
            labels=list(map(lambda x: x.capitalize(), tiers)), 
            autopct=lbl_fcn, 
            colors=colors, 
            startangle=15)
    plt.title(str(rounds_info_dict[pick_map]['Name'] if pick_map in rounds_info_dict.keys() else pick_map)+": Bonus Tiers")

    return vc


# pie chart for final map wins
def finalMapWinsPie(finals_df):
    map_wins = finals_df[finals_df['Qualified']]['Map'].value_counts()

    plt.pie(map_wins, 
            labels=list(map(lambda x: rounds_info_dict[x]['Name'] if x in rounds_info_dict.keys() else x, map_wins.index)), 
            autopct=lambda x: int(map_wins.sum() * x / 100))
    plt.suptitle('Wins by Final');
    return map_wins


# pie chart for shows
def showWinsPie(shows_df):
    show_wins = shows_df[shows_df['Crowns'] == 1]['Game Mode'].value_counts()

    plt.pie(show_wins, 
            labels=list(map(lambda x: show_type_dict[x] if x in show_type_dict.keys() else x, show_wins.index)), 
            autopct=lambda x: int(show_wins.sum() * x / 100), 
            shadow=True, 
            # explode=[1 if x == show_wins.max() else 0 for x in show_wins], 
           )
    plt.title('Wins by Game Mode');
    return show_wins


# plays vs wins and losses by final map
# https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html#sphx-glr-gallery-pie-and-polar-charts-nested-pie-py
# https://matplotlib.org/3.1.0/gallery/text_labels_and_annotations/custom_legends.html
# https://stackoverflow.com/questions/21572870/matplotlib-percent-label-position-in-pie-chart (pct position)
def finalsWinsLossesPie(finals_df, regular=True, total_num=True):
    finals = finals_df['Map'].value_counts()
    final_wins = finals_df[finals_df['Qualified']]['Map'].value_counts()
    f_df = pd.DataFrame([finals, final_wins], index=['overall', 'wins']).T.fillna(0).astype(int)
    f_df['loss'] = f_df['overall'] - f_df['wins']

    if regular:
        for x in f_df.index:
            if 'event_only_final' in x:
                f_df = f_df.drop(x)

    fig, ax = plt.subplots(figsize=(6,6))
    cmap = plt.get_cmap('tab20')
    if total_num:
        plt.pie(f_df['overall'], 
                labels=list(map(lambda x: rounds_info_dict[x]['Name'] if x in rounds_info_dict.keys() else x, f_df.index)), 
                radius=1.2, 
                colors=cmap([i*2 for i in range(len(f_df))]), 
                wedgeprops={'edgecolor':'w', 'width':.4}, 
                autopct=lambda x: int(round(f_df['overall'].sum() * x / 100)), 
                pctdistance=.835,
               );
    else:
        plt.pie(f_df['overall'], 
                labels=list(map(lambda x: rounds_info_dict[x]['Name'] if x in rounds_info_dict.keys() else x, f_df.index)), 
                radius=1.2, 
                colors=cmap([i*2 for i in range(len(f_df))]), 
                wedgeprops={'edgecolor':'w', 'width':.4}, 
               );
        
    plt.pie(np.array(f_df[['wins', 'loss']]).flatten(), 
            radius=.8, 
            colors=cmap([i for i in range(2*len(f_df))]), 
            wedgeprops={'edgecolor':'w', 'width':.6}
           );
    plt.title('Wins and Losses by Final')

    legend_elements = [Patch(facecolor=cmap([0])[0][:3], edgecolor=cmap([0])[0][:3],
                             label='Outer: Total Plays'), 
                       Patch(facecolor=cmap([0])[0][:3], edgecolor=cmap([0])[0][:3],
                             label='Inner: Wins'), 
                       Patch(facecolor=cmap([1])[0][:3], edgecolor=cmap([1])[0][:3],
                             label='Inner: Losses')]

    ax.legend(handles=legend_elements, bbox_to_anchor=(1, .8))
    ax.set(aspect="equal")
    return f_df


# fcn to make various pie charts for starting maps
def startingRacesPie(rounds_df, inner='Qualified', title='Qualification by Starting Races', 
                     outer_title='Total Plays', inner_pos_title='Qualified', inner_neg_title='Disqualified', 
                     total_num=True, pie_size=(6,6)):
    sr_df = rounds_df[rounds_df['Map'].isin(starting_races)]
    sr_total = sr_df['Map'].value_counts()
    if inner == 'Qualified':
        sr_qual = sr_df[sr_df['Qualified']]['Map'].value_counts()
    else:
        sr_qual = sr_df[sr_df['BadgeId'] == inner]['Map'].value_counts()
    
    s_df = pd.DataFrame([sr_total, sr_qual], index=['overall', 'pos']).T.fillna(0).astype(int)
    s_df['neg'] = s_df['overall'] - s_df['pos']

    fig, ax = plt.subplots(figsize=pie_size)
    cmap = plt.get_cmap('tab20')
    if total_num:
        plt.pie(s_df['overall'], 
                labels=list(map(lambda x: rounds_info_dict[x]['Name'] if x in rounds_info_dict.keys() else x, s_df.index)), 
                radius=1.2, 
                colors=cmap([i*2 for i in range(len(s_df))]), 
                wedgeprops={'edgecolor':'w', 'width':.4}, 
                autopct=lambda x: int(round(s_df['overall'].sum() * x / 100)), 
                pctdistance=.835,
               );
    else:
        plt.pie(s_df['overall'], 
                labels=list(map(lambda x: rounds_info_dict[x]['Name'] if x in rounds_info_dict.keys() else x, s_df.index)), 
                radius=1.2, 
                colors=cmap([i*2 for i in range(len(s_df))]), 
                wedgeprops={'edgecolor':'w', 'width':.4}, 
               );
        
    plt.pie(np.array(s_df[['pos', 'neg']]).flatten(), 
            radius=.8, 
            colors=cmap([i for i in range(2*len(s_df))]), 
            wedgeprops={'edgecolor':'w', 'width':.6}
           );
    plt.suptitle(title)

    legend_elements = [Patch(facecolor=cmap([0])[0][:3], edgecolor=cmap([0])[0][:3],
                             label='Outer: {}'.format(outer_title)), 
                       Patch(facecolor=cmap([0])[0][:3], edgecolor=cmap([0])[0][:3],
                             label='Inner: {}'.format(inner_pos_title)), 
                       Patch(facecolor=cmap([1])[0][:3], edgecolor=cmap([1])[0][:3],
                             label='Inner: {}'.format(inner_neg_title))]

    ax.legend(handles=legend_elements, bbox_to_anchor=(1, .8))
    ax.set(aspect="equal")
    return s_df


# Get a bar graph for average time per win by season and total
def minutesPerWinBar(shows_info_df):
    fig, ax = plt.subplots(figsize=(7,6))
    plt.bar(shows_info_df.index.astype(str).tolist(), shows_info_df['Minutes Per Win'], color='#2FC1BE')
    plt.suptitle('Minutes Per Win by Season')
    plt.xlabel('Season')
    plt.ylabel('Minutes')

    def autolabel(rects):
            for i, rect in enumerate(rects):
                height = rect.get_height()
                ax.annotate('{}'.format(str(shows_info_df['Total Wins'].iloc[i]))+' wins',
                            xy=(rect.get_x() + rect.get_width() / 2, height-10),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

    autolabel(ax.containers[0])
    return


# Get a bar chart for wins by season
def winsBySeasonBar(shows_info_df):
    fig, ax = plt.subplots(figsize=(7,6))
    plt.bar(shows_info_df.index.astype(str).tolist(), shows_info_df['Total Wins'], color='#358EDC')
    plt.suptitle('Wins by Season')
    plt.xlabel('Season')
    plt.ylabel('Wins')

    def autolabel(rects):
            for i, rect in enumerate(rects):
                height = rect.get_height()
                ax.annotate('{}'.format(shows_info_df['Total Wins'].iloc[i]),
                            xy=(rect.get_x() + rect.get_width() / 2, height-2),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

    autolabel(ax.containers[0])
    return


# Get a pie chart for success in playlists that are of the 'same' final
def specialShowsPie(special_show, shows_df, explode=False, percent=False):
    round_counts = shows_df[ shows_df['Game Mode'].str.contains(special_show) ]['Rounds'].value_counts()
    wins = shows_df[ shows_df['Game Mode'].str.contains(special_show) ]['Crowns'].astype(bool).sum()
    
    elim_dict = {'Wins': wins}
    explode_list = [1, 0, 0, 0]
    if len(round_counts) == 4:
        elim_dict['Eliminated: Final'] = round_counts[4] - wins
        elim_dict['Eliminated: 3rd Round'] = round_counts[3]
        explode_list.append(0)
    else:
        elim_dict['Eliminated: Final'] = round_counts[3] - wins
        
    elim_dict['Eliminated: 2nd Round'] = round_counts[2]
    elim_dict['Eliminated: 1st Round'] = round_counts[1]
    
    # plot it
    if percent:
        lbl_fcn = lambda x: "{:.2f}%".format(x)
    else:
        lbl_fcn = lambda x: int(round(round_counts.sum() * x / 100))
    
    # pie chart
    plt.rcParams['font.size'] = 14
    fig, ax = plt.subplots(figsize=(7,7))
    plt.pie(elim_dict.values(), 
            labels=elim_dict.keys(), 
            autopct=lbl_fcn,
            colors=['#DFA517', '#1189BB', '#C00F27', '#2AB311', '#9E1EA8'], 
            startangle=15,
            wedgeprops={'edgecolor':'w'},
            explode=explode_list if explode else None,
           )
    plt.title([show_type_dict[key] for key in list(show_type_dict.keys()) if special_show in key][0].title())
    return

