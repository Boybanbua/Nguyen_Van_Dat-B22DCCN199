import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time

url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

tables_link = soup.find_all('table')  # Tìm tất cả các bảng
table_link = tables_link[0]
rows = table_link.find_all('tr') 

team_links = []
team_names = []

for row in rows:
    team_cell = row.find('th', {'class': 'left', 'data-stat': 'team'})
    if team_cell:
        a_tag = team_cell.find('a') 
        if a_tag and 'href' in a_tag.attrs:
            link = 'https://fbref.com/' + a_tag['href']
            team_links.append(link)  # Thêm link vào danh sách
    team_tag = row.find('th', {'data-stat': 'team'})  
    if team_tag and team_tag.find('a'):  
        team_name = team_tag.find('a').text.strip()
        team_names.append(team_name) # Thêm tên đội vào danh sách


players_data = []
goalkeeping_data = []
shooting_data = []
passing_data = []
passtype_data = []
goal_shot_data = []
defensive_data = []
playing_time_data = []
miscellaneous_data = []
possession_data = []

i = 0 # Chỉ số để lấy tên của các đội nằm trong team_names
for link in team_links:
    response = requests.get(link)
    time.sleep(4) # Delay thoi gian khong thi bi chan
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')  # Tìm tất cả các bảng
    table = tables[0]  # Bảng Standard Stats

    # Bước 3: Lấy tất cả các hàng (tr) trong bảng
    rows = table.find_all('tr') 
    for row in rows[:-2]: # bỏ đi 2 hàng cuối do không phải cầu thủ

        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                
                # Playing time
                'matches_played': row.find('td', {'data-stat': 'games'}).text.strip() or 'N/a',
                'starts': row.find('td', {'data-stat': 'games_starts'}).text.strip() or 'N/a',
                'minutes': row.find('td', {'data-stat': 'minutes'}).text.strip() or 'N/a',

                # Performance
                'non_penalty_goals': row.find('td', {'data-stat': 'goals'}).text.strip() or 'N/a',
                'penalty_goals': row.find('td', {'data-stat': 'pens_made'}).text.strip() or 'N/a',
                'assists': row.find('td', {'data-stat': 'assists'}).text.strip() or 'N/a',
                'yellow_cards': row.find('td', {'data-stat': 'cards_yellow'}).text.strip() or 'N/a',
                'red_cards': row.find('td', {'data-stat': 'cards_red'}).text.strip() or 'N/a',

                # Expected
                'xG': row.find('td', {'data-stat': 'xg'}).text.strip() or 'N/a',
                'npxG': row.find('td', {'data-stat': 'npxg'}).text.strip() or 'N/a',
                'xAG': row.find('td', {'data-stat': 'xg_assist'}).text.strip() or 'N/a',

                # Progression
                'prgC': row.find('td', {'data-stat': 'progressive_carries'}).text.strip() or 'N/a',
                'prgP': row.find('td', {'data-stat': 'progressive_passes'}).text.strip() or 'N/a',
                'prgR': row.find('td', {'data-stat': 'progressive_passes_received'}).text.strip() or 'N/a',

                # Per 90 minutes
                'gls_per90': row.find('td', {'data-stat': 'goals_per90'}).text.strip() or 'N/a',
                'ast_per90': row.find('td', {'data-stat': 'assists_per90'}).text.strip() or 'N/a',
                'g+a_per90': row.find('td', {'data-stat': 'goals_assists_per90'}).text.strip() or 'N/a',
                'g-pk_per90': row.find('td', {'data-stat': 'goals_pens_per90'}).text.strip() or 'N/a',
                'g+a-pk_per90': row.find('td', {'data-stat': 'goals_assists_pens_per90'}).text.strip() or 'N/a',
                'xg_per90': row.find('td', {'data-stat': 'xg_per90'}).text.strip() or 'N/a',
                'xag_per90': row.find('td', {'data-stat': 'xg_assist_per90'}).text.strip() or 'N/a',
                'xg+xag_per90': row.find('td', {'data-stat': 'xg_xg_assist_per90'}).text.strip() or 'N/a',
                'npxg_per90': row.find('td', {'data-stat': 'npxg_per90'}).text.strip() or 'N/a',
                'npxg+xag_per90': row.find('td', {'data-stat': 'npxg_xg_assist_per90'}).text.strip() or 'N/a'
            }
            players_data.append(player_info)

    table = tables[2]  # Bảng Goalkeeping
    rows = table.find_all('tr')
    for row in rows[:-2]:

        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90

            player_info = {
                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),

                'GA': row.find('td', {'data-stat': 'gk_goals_against'}).text.strip() or 'N/a',
                'GA90': row.find('td', {'data-stat': 'gk_goals_against_per90'}).text.strip() or 'N/a',
                'SoTA': row.find('td', {'data-stat': 'gk_shots_on_target_against'}).text.strip() or 'N/a',
                'Saves': row.find('td', {'data-stat': 'gk_saves'}).text.strip() or 'N/a',
                'Save%': row.find('td', {'data-stat': 'gk_save_pct'}).text.strip() or 'N/a',
                'W': row.find('td', {'data-stat': 'gk_wins'}).text.strip() or 'N/a',
                'D': row.find('td', {'data-stat': 'gk_ties'}).text.strip() or 'N/a',
                'L': row.find('td', {'data-stat': 'gk_losses'}).text.strip() or 'N/a',
                'CS': row.find('td', {'data-stat': 'gk_clean_sheets'}).text.strip() or 'N/a',
                'CS%': row.find('td', {'data-stat': 'gk_clean_sheets_pct'}).text.strip() or 'N/a',
                'PKatt': row.find('td', {'data-stat': 'gk_pens_att'}).text.strip() or 'N/a',
                'PKA': row.find('td', {'data-stat': 'gk_pens_allowed'}).text.strip() or 'N/a',
                'PKsv': row.find('td', {'data-stat': 'gk_pens_saved'}).text.strip() or 'N/a',
                'PKm': row.find('td', {'data-stat': 'gk_pens_missed'}).text.strip() or 'N/a',
                'Save%PK': row.find('td', {'data-stat': 'gk_pens_save_pct'}).text.strip() or 'N/a',
            }
            goalkeeping_data.append(player_info)


    table = tables[4]  # Shooting Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:

        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {
                
                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),


                'Gls': row.find('td', {'data-stat': 'goals'}).text.strip() or 'N/a',
                'Sh': row.find('td', {'data-stat': 'shots'}).text.strip()  or 'N/a',
                'SoT': row.find('td', {'data-stat': 'shots_on_target'}).text.strip()  or 'N/a',
                'SoT%': row.find('td', {'data-stat': 'shots_on_target_pct'}).text.strip()  or 'N/a',
                'Sh/90': row.find('td', {'data-stat': 'shots_per90'}).text.strip()  or 'N/a',
                'SoT/90': row.find('td', {'data-stat': 'shots_on_target_per90'}).text.strip()  or 'N/a',
                'G/Sh': row.find('td', {'data-stat': 'goals_per_shot'}).text.strip()  or 'N/a',
                'G/SoT': row.find('td', {'data-stat': 'goals_per_shot_on_target'}).text.strip()  or 'N/a',
                'Dist': row.find('td', {'data-stat': 'average_shot_distance'}).text.strip()  or 'N/a',
                'FK': row.find('td', {'data-stat': 'shots_free_kicks'}).text.strip()  or 'N/a',
                'PK': row.find('td', {'data-stat': 'pens_made'}).text.strip()  or 'N/a',
                'PKatt': row.find('td', {'data-stat': 'pens_att'}).text.strip()  or 'N/a',


                'xG': row.find('td', {'data-stat': 'xg'}).text.strip()  or 'N/a',
                'npxG': row.find('td', {'data-stat': 'npxg'}).text.strip()  or 'N/a',
                'npxG/Sh': row.find('td', {'data-stat': 'npxg_per_shot'}).text.strip()  or 'N/a',
                'G-xG': row.find('td', {'data-stat': 'xg_net'}).text.strip()  or 'N/a',
                'np:G-xG': row.find('td', {'data-stat': 'npxg_net'}).text.strip()  or 'N/a',
            }
            shooting_data.append(player_info)


    table = tables[5]  # Passing  Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:
        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),

                'Cmp': row.find('td', {'data-stat': 'passes_completed'}).text.strip() or 'N/a',
                'Att': row.find('td', {'data-stat': 'passes'}).text.strip() or 'N/a',
                'Cmp%': row.find('td', {'data-stat': 'passes_pct'}).text.strip() or 'N/a',
                'TotDist': row.find('td', {'data-stat': 'passes_total_distance'}).text.strip() or 'N/a',
                'PrgDist': row.find('td', {'data-stat': 'passes_progressive_distance'}).text.strip() or 'N/a',

                'Cmp_Short': row.find('td', {'data-stat': 'passes_completed_short'}).text.strip() or 'N/a',
                'Att_Short': row.find('td', {'data-stat': 'passes_short'}).text.strip() or 'N/a',
                'Cmp%_Short': row.find('td', {'data-stat': 'passes_pct_short'}).text.strip() or 'N/a',

                'Cmp_Medium': row.find('td', {'data-stat': 'passes_completed_medium'}).text.strip() or 'N/a',
                'Att_Medium': row.find('td', {'data-stat': 'passes_medium'}).text.strip() or 'N/a',
                'Cmp%_Medium': row.find('td', {'data-stat': 'passes_pct_medium'}).text.strip() or 'N/a',

                'Cmp_Long': row.find('td', {'data-stat': 'passes_completed_long'}).text.strip() or 'N/a',
                'Att_Long': row.find('td', {'data-stat': 'passes_long'}).text.strip() or 'N/a',
                'Cmp%_Long': row.find('td', {'data-stat': 'passes_pct_long'}).text.strip() or 'N/a',

                'Ast': row.find('td', {'data-stat': 'assists'}).text.strip() or 'N/a',
                'xAG': row.find('td', {'data-stat': 'xg_assist'}).text.strip() or 'N/a',
                'xA': row.find('td', {'data-stat': 'pass_xa'}).text.strip() or 'N/a',
                'A-xAG': row.find('td', {'data-stat': 'xg_assist_net'}).text.strip() or 'N/a',
                'KP': row.find('td', {'data-stat': 'assisted_shots'}).text.strip() or 'N/a',
                '1/3': row.find('td', {'data-stat': 'passes_into_final_third'}).text.strip() or 'N/a',
                'PPA': row.find('td', {'data-stat': 'passes_into_penalty_area'}).text.strip() or 'N/a',
                'CrsPA': row.find('td', {'data-stat': 'crosses_into_penalty_area'}).text.strip() or 'N/a',
                'PrgP': row.find('td', {'data-stat': 'progressive_passes'}).text.strip() or 'N/a'
            }
            passing_data.append(player_info)


    table = tables[6]  # Pass Arsenal:
    rows = table.find_all('tr')
    for row in rows[:-2]:

        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),


                'Live': row.find('td', {'data-stat': 'passes_live'}).text.strip() or 'N/a',
                'Dead': row.find('td', {'data-stat': 'passes_dead'}).text.strip() or 'N/a',
                'FK': row.find('td', {'data-stat': 'passes_free_kicks'}).text.strip() or 'N/a',
                'TB': row.find('td', {'data-stat': 'through_balls'}).text.strip() or 'N/a',
                'Sw': row.find('td', {'data-stat': 'passes_switches'}).text.strip() or 'N/a',
                'Crs': row.find('td', {'data-stat': 'crosses'}).text.strip() or 'N/a',
                'TI': row.find('td', {'data-stat': 'throw_ins'}).text.strip() or 'N/a',
                'CK': row.find('td', {'data-stat': 'corner_kicks'}).text.strip() or 'N/a',


                'CK_In': row.find('td', {'data-stat': 'corner_kicks_in'}).text.strip() or 'N/a',
                'CK_Out': row.find('td', {'data-stat': 'corner_kicks_out'}).text.strip() or 'N/a',
                'CK_Str': row.find('td', {'data-stat': 'corner_kicks_straight'}).text.strip() or 'N/a',


                'Cmp': row.find('td', {'data-stat': 'passes_completed'}).text.strip() or 'N/a',
                'Off': row.find('td', {'data-stat': 'passes_offsides'}).text.strip() or 'N/a',
                'Blocks': row.find('td', {'data-stat': 'passes_blocked'}).text.strip() or 'N/a'
            }
            passtype_data.append(player_info)


    table = tables[7]  # Goal and Shot Creation Arsenal:
    rows = table.find_all('tr')
    for row in rows[:-2]:

        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                

                'SCA': row.find('td', {'data-stat': 'sca'}).text.strip() or 'N/a',
                'SCA90': row.find('td', {'data-stat': 'sca_per90'}).text.strip() or 'N/a',
                
                'PassLive': row.find('td', {'data-stat': 'sca_passes_live'}).text.strip() or 'N/a',
                'PassDead': row.find('td', {'data-stat': 'sca_passes_dead'}).text.strip() or 'N/a',
                'TO': row.find('td', {'data-stat': 'sca_take_ons'}).text.strip() or 'N/a',
                'Sh': row.find('td', {'data-stat': 'sca_shots'}).text.strip() or 'N/a',
                'Fld': row.find('td', {'data-stat': 'sca_fouled'}).text.strip() or 'N/a',
                'Def': row.find('td', {'data-stat': 'sca_defense'}).text.strip() or 'N/a',
                
                'GCA': row.find('td', {'data-stat': 'gca'}).text.strip() or 'N/a', 
                'GCA90': row.find('td', {'data-stat': 'gca_per90'}).text.strip() or 'N/a',
                'GCA_PassLive': row.find('td', {'data-stat': 'gca_passes_live'}).text.strip() or 'N/a',
                'GCA_PassDead': row.find('td', {'data-stat': 'gca_passes_dead'}).text.strip() or 'N/a',
                'GCA_TO': row.find('td', {'data-stat': 'gca_take_ons'}).text.strip() or 'N/a',
                'GCA_Sh': row.find('td', {'data-stat': 'gca_shots'}).text.strip() or 'N/a',
                'GCA_Fld': row.find('td', {'data-stat': 'gca_fouled'}).text.strip() or 'N/a',
                'GCA_Def': row.find('td', {'data-stat': 'gca_defense'}).text.strip() or 'N/a'
            }
            goal_shot_data.append(player_info)


    table = tables[8]  # Defensive Actions  Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:
        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                
                'Tkl': row.find('td', {'data-stat': 'tackles'}).text.strip() or 'N/a',
                'TklW': row.find('td', {'data-stat': 'tackles_won'}).text.strip() or 'N/a',
                'Def_3rd': row.find('td', {'data-stat': 'tackles_def_3rd'}).text.strip() or 'N/a',
                'Mid_3rd': row.find('td', {'data-stat': 'tackles_mid_3rd'}).text.strip() or 'N/a',
                'Att_3rd': row.find('td', {'data-stat': 'tackles_att_3rd'}).text.strip() or 'N/a',


                'Challenge_Tkl': row.find('td', {'data-stat': 'challenge_tackles'}).text.strip() or 'N/a',
                'Challenges_Att': row.find('td', {'data-stat': 'challenges'}).text.strip() or 'N/a',
                'Tkl_pct': row.find('td', {'data-stat': 'challenge_tackles_pct'}).text.strip() or 'N/a',
                'Challenges_Lost': row.find('td', {'data-stat': 'challenges_lost'}).text.strip() or 'N/a',


                'Blocks': row.find('td', {'data-stat': 'blocks'}).text.strip() or 'N/a',
                'Blocked_Shots': row.find('td', {'data-stat': 'blocked_shots'}).text.strip() or 'N/a',
                'Blocked_Passes': row.find('td', {'data-stat': 'blocked_passes'}).text.strip() or 'N/a',
                'Interceptions': row.find('td', {'data-stat': 'interceptions'}).text.strip() or 'N/a',
                'Tkl_Int': row.find('td', {'data-stat': 'tackles_interceptions'}).text.strip() or 'N/a',
                'Clearances': row.find('td', {'data-stat': 'clearances'}).text.strip() or 'N/a',
                'Errors': row.find('td', {'data-stat': 'errors'}).text.strip() or 'N/a'
            }
            defensive_data.append(player_info)


    table = tables[9]  # Possession Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:
        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                
                'Touches': row.find('td', {'data-stat': 'touches'}).text.strip() or 'N/a',
                'Def_Pen': row.find('td', {'data-stat': 'touches_def_pen_area'}).text.strip() or 'N/a',
                'Def_3rd': row.find('td', {'data-stat': 'touches_def_3rd'}).text.strip() or 'N/a',
                'Mid_3rd': row.find('td', {'data-stat': 'touches_mid_3rd'}).text.strip() or 'N/a',
                'Att_3rd': row.find('td', {'data-stat': 'touches_att_3rd'}).text.strip() or 'N/a',
                'Att_Pen': row.find('td', {'data-stat': 'touches_att_pen_area'}).text.strip() or 'N/a',
                'Live': row.find('td', {'data-stat': 'touches_live_ball'}).text.strip() or 'N/a',


                'TakeOn_Att': row.find('td', {'data-stat': 'take_ons'}).text.strip() or 'N/a',
                'TakeOn_Succ': row.find('td', {'data-stat': 'take_ons_won'}).text.strip() or 'N/a',
                'TakeOn_Succ_pct': row.find('td', {'data-stat': 'take_ons_won_pct'}).text.strip() or 'N/a',
                'TakeOn_Tkld': row.find('td', {'data-stat': 'take_ons_tackled'}).text.strip() or 'N/a',
                'TakeOn_Tkld_pct': row.find('td', {'data-stat': 'take_ons_tackled_pct'}).text.strip() or 'N/a',


                'Carries': row.find('td', {'data-stat': 'carries'}).text.strip() or 'N/a',
                'TotDist': row.find('td', {'data-stat': 'carries_distance'}).text.strip() or 'N/a',
                'ProDist': row.find('td', {'data-stat': 'carries_progressive_distance'}).text.strip() or 'N/a',
                'ProgC': row.find('td', {'data-stat': 'progressive_carries'}).text.strip() or 'N/a',
                '1/3': row.find('td', {'data-stat': 'carries_into_final_third'}).text.strip() or 'N/a',
                'CPA': row.find('td', {'data-stat': 'carries_into_penalty_area'}).text.strip() or 'N/a',
                'Mis': row.find('td', {'data-stat': 'miscontrols'}).text.strip() or 'N/a',
                'Dis': row.find('td', {'data-stat': 'dispossessed'}).text.strip() or 'N/a',


                'Rec': row.find('td', {'data-stat': 'passes_received'}).text.strip() or 'N/a',
                'PrgR': row.find('td', {'data-stat': 'progressive_passes_received'}).text.strip() or 'N/a'
            }
            possession_data.append(player_info)



    table = tables[10]  # 10 bảng: Playing Time Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:
        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                
                'Starts': row.find('td', {'data-stat': 'games_starts'}).text.strip() or 'N/a',
                'Mn/Start': row.find('td', {'data-stat': 'minutes_per_start'}).text.strip() or 'N/a',
                'Compl': row.find('td', {'data-stat': 'games_complete'}).text.strip() or 'N/a',
                'Subs': row.find('td', {'data-stat': 'games_subs'}).text.strip() or 'N/a',
                'Mn/Sub': row.find('td', {'data-stat': 'minutes_per_sub'}).text.strip() or 'N/a',
                'unSub': row.find('td', {'data-stat': 'unused_subs'}).text.strip() or 'N/a',
                'PPM': row.find('td', {'data-stat': 'points_per_game'}).text.strip() or 'N/a',
                'onG': row.find('td', {'data-stat': 'on_goals_for'}).text.strip() or 'N/a',
                'onGA': row.find('td', {'data-stat': 'on_goals_against'}).text.strip() or'N/a',
                'onxG': row.find('td', {'data-stat': 'on_xg_for'}).text.strip() or 'N/a',
                'onxGA': row.find('td', {'data-stat': 'on_xg_against'}).text.strip() or 'N/a',
            }
            playing_time_data.append(player_info)


    table = tables[11]  # 11 bảng: Miscellaneous Stats Arsenal
    rows = table.find_all('tr')
    for row in rows[:-2]:
        minutes = row.find('td', {'data-stat': 'minutes_90s'}) # để kiểm tra xem cầu thủ có thi đấu trên 90p hay không
        if minutes and minutes.text.strip() and float(minutes.text.strip()) >= 1: # do đây là 90s divided 90
            player_info = {

                'Player' : row.find('th', {'data-stat': 'player'}).text.strip() ,
                'Nation': row.find('td', {'data-stat': 'nationality'}).text.strip().split()[-1],
                'Team': team_names[i],
                'Pos': row.find('td', {'data-stat': 'position'}).text.strip(),
                'Age': row.find('td', {'data-stat': 'age'}).text.strip(),
                
                'Fls': row.find('td', {'data-stat': 'fouls'}).text.strip() or 'N/a',  
                'Fld': row.find('td', {'data-stat': 'fouled'}).text.strip() or 'N/a',  
                'Off': row.find('td', {'data-stat': 'offsides'}).text.strip() or 'N/a',  
                'Crs': row.find('td', {'data-stat': 'crosses'}).text.strip() or 'N/a',  
                'OG': row.find('td', {'data-stat': 'own_goals'}).text.strip() or 'N/a',  
                'Recov': row.find('td', {'data-stat': 'ball_recoveries'}).text.strip() or 'N/a',  
                'Won': row.find('td', {'data-stat': 'aerials_won'}).text.strip() or 'N/a',  
                'Lost': row.find('td', {'data-stat': 'aerials_lost'}).text.strip() or 'N/a',  
                'Won%': row.find('td', {'data-stat': 'aerials_won_pct'}).text.strip() or 'N/a',  

            }
            miscellaneous_data.append(player_info)
    i += 1 # tăng chỉ số  


player = pd.DataFrame(players_data)
goal = pd.DataFrame(goalkeeping_data)
shoot = pd.DataFrame(shooting_data)
passing = pd.DataFrame(passing_data)
passtype = pd.DataFrame(passtype_data)
goal_shot = pd.DataFrame(goal_shot_data)
defensive = pd.DataFrame(defensive_data)
playing_time = pd.DataFrame(playing_time_data)
miscellaneous = pd.DataFrame(miscellaneous_data)
possession = pd.DataFrame(possession_data)


# Danh sách các DataFrame
dataframes = [goal, shoot, passing, passtype, goal_shot, defensive, possession, playing_time, miscellaneous]
merged_df = player

# Gộp từng DataFrame trong danh sách
for df in dataframes:
    merged_df = pd.merge(merged_df, df, on=["Player", "Nation", "Team", "Pos", "Age"], how="left")

# Tách tên đầu tiên từ cột 'Player'
merged_df['First Name'] = merged_df['Player'].str.split().str[0]  # Lấy phần đầu tiên

# Sắp xếp DataFrame theo 'First Name' và 'Age'
sorted_df = merged_df.sort_values(by=['First Name', 'Age'], ascending=[True, False])

# Xóa cột 'First Name'
sorted_df = sorted_df.drop(columns=['First Name'])
# Điền các giá trị rỗng là N/a
sorted_df = sorted_df.fillna("N/a")
# Ghi DataFrame đã sắp xếp vào tệp results CSV
sorted_df.to_csv('D:/results.csv', index=False, encoding='utf-8')