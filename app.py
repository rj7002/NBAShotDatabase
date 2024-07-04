import datetime
import pandas as pd
import streamlit as st
import requests
import time
from nba_api.stats.endpoints import PlayByPlay
from nba_api.stats.endpoints import PlayByPlayV3
from nba_api.stats.endpoints import PlayByPlayV2
import json
import pandas as pd
from nba_api.stats.endpoints import ShotChartDetail
from nba_api.stats.endpoints import TeamGameLogs
from datetime import datetime
from datetime import date
import plotly.graph_objects as go
import numpy as np

st.set_page_config(layout='wide',page_title="NBA Shot Database",page_icon='🏀')

def display_player_image(player_id, width2, caption2):
    # Construct the URL for the player image using the player ID
    image_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
    print(image_url)
    
    
    # Check if the image URL returns a successful response
    response = requests.head(image_url)
    
    if response.status_code == 200:
        # If image is available, display it
        st.markdown(
    f'<div style="display: flex; flex-direction: column; align-items: center;">'
    f'<img src="{image_url}" style="width: {width2}px;">'
    f'<p style="text-align: center; font-size: 20px;">{caption2}</p>'
    f'</div>',
    unsafe_allow_html=True
)

def map_team_to_abbreviation(team_name):
    team_mapping = {
        'BOS': 'bos',
        'BRK': 'bkn',
        'NYK': 'ny',
        'PHI': 'phi',
        'TOR': 'tor',
        'CHI': 'chi',
        'CLE': 'cle',
        'DET': 'det',
        'IND': 'ind',
        'MIL': 'mil',
        'DEN': 'den',
        'MIN': 'min',
        'OKC': 'okc',
        'POR': 'por',
        'UTA': 'utah',
        'GSW': 'gs',
        'LAC': 'lac',
        'LAL': 'lal',
        'PHO': 'phx',
        'SAC': 'sac',
        'ATL': 'atl',
        'CHA': 'cha',
        'MIA': 'mia',
        'ORL': 'orl',
        'WAS': 'wsh',
        'DAL': 'dal',
        'HOU': 'hou',
        'MEM': 'mem',
        'NOP': 'no',
        'SAS': 'sa'
    }
    
    return team_mapping.get(team_name, 'Unknown Team')

def display_team_image(teamname, width2):
    # Construct the URL for the player image using the player ID
    image_url = f"https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/{teamname}.png&scale=crop&cquality=40&location=origin&w=80&h=80"
    print(image_url)
    
    
    # Check if the image URL returns a successful response
    response = requests.head(image_url)
    
    if response.status_code == 200:
        # If image is available, display it
        st.markdown(
    f'<div style="display: flex; flex-direction: column; align-items: center;">'
    f'<img src="{image_url}" style="width: {width2}px;">'
    f'<p style="text-align: center; font-size: 20px;"></p>'
    f'</div>',
    unsafe_allow_html=True
)
    
    
        # st.image(image_url, width=width2, caption=caption2)
    else:
        image_url = "https://cdn.nba.com/headshots/nba/latest/1040x760/fallback.png"
        st.markdown(
        f'<div style="display: flex; flex-direction: column; align-items: center;">'
        f'<img src="{image_url}" style="width: {width2}px;">'
        f'<p style="text-align: center;font-size: larger;">{"Image Unavailable"}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

def draw_plotly_court(fig, fig_width=600, margins=10):
        
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "black"
    main_line_col = "black"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333'
                
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333'
                
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=2),
                # fillcolor='#333333'
                
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=2),
                # fillcolor='#dddddd'
                
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=2)
                
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=2),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=2),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=2),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=2)),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=2)),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2)
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2)
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=2)
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=2)
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=2)
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=2)),

        ]
    )
    return True

    



st.markdown("<h1 style='text-align: center;'>NBA Shot Database</h1>", unsafe_allow_html=True)
# input_csv = 'nba_play_by_play.csv'  # Replace with your actual CSV file path
# output_csv = 'nba_play_by_play.csv'  # Replace with desired output file path
current_year = date.today().year

 


# Function to fetch NBA game IDs
def fetch_game_ids(season):
    # Make a GET request to the NBA schedule JSON endpoint
    r = requests.get(f"http://data.nba.com/data/10s/v{season}/json/mobile_teams/nba/{season+1}/league/00_full_schedule.json")

    # Check if the request was successful (status code 200)
    if r.status_code == 200:
        # Parse JSON data
        data = r.json()
        
        # Extract game IDs (gid) from the JSON data
        gids = [game['gid'] for game in data['lscd'][0]['mscd']['g']]
        
        return gids
    else:
        # Print an error message if the request was unsuccessful
        st.error(f"Failed to retrieve data: {r.status_code} - {r.reason}")
        return None



seasons = list(range(2014, current_year))
totals = st.sidebar.toggle('All NBA')

# Create a selectbox for selecting a season
szn = st.selectbox('Select a season', [''] + seasons)
if szn != '':
    
    szn2 = szn+1
    season = str(szn) + '-' + str(szn2)[2:]
    
    if totals:
        typeszn = st.checkbox('Playoffs?')
        if typeszn:
            type = 'Playoffs'
        else:
            type = 'Regular Season'
        response = ShotChartDetail(
            team_id=0,
            player_id=0,
            season_nullable=season,
            season_type_all_star=type,
            context_measure_simple = 'FGA'
        )

        content = json.loads(response.get_json())

        results = content['resultSets'][0]
        headers = results['headers']
        rows = results['rowSet']
        df = pd.DataFrame(rows)
        df.columns = headers

        # write to csv file
        df['SHOT_RESULT'] = df['EVENT_TYPE'].apply(lambda x: x.split()[0])
        shots = df['ACTION_TYPE'].unique()
        Makes = st.sidebar.toggle('Make/Miss')
        if Makes == 1:
            makes = st.sidebar.selectbox('', ['Made', 'Missed'])
            if makes == 'Made':
                fmakes = 1
                df = df[df['SHOT_MADE_FLAG'] == fmakes]
            elif makes == 'Missed':
                fmakes = 0
                df = df[df['SHOT_MADE_FLAG'] == fmakes]
        Shottype = st.sidebar.toggle('Shot Type')
        if Shottype == 1:
            shottype = st.sidebar.multiselect('', shots)
            df = df[df['ACTION_TYPE'].isin(shottype)]
        Points = st.sidebar.toggle('Points')
        allpoints = df['SHOT_TYPE'].unique()
        if Points == 1:
            points = st.sidebar.selectbox('', allpoints)
            df = df[df['SHOT_TYPE'] == points]
        Quarter = st.sidebar.toggle('Quarter')
        if Quarter == 1:
            df['QUARTER'] = df['PERIOD']
            quarts = df['QUARTER'].unique()
            quart = st.sidebar.multiselect('',quarts)
            df = df[df['QUARTER'].isin(quart)]
        Time = st.sidebar.toggle('Time')
        if Time == 1:
            timemin, timemax = st.sidebar.slider("Time Remaining (Minutes)", 0, 15, (0, 15))
            df = df[(df['MINUTES_REMAINING'] >= timemin) & (df['MINUTES_REMAINING'] <= timemax)]
        Shotdist = st.sidebar.toggle('Shot Distance')
        if Shotdist == 1:
            shotdistance_min, shotdistance_max = st.sidebar.slider("Shot Distance", 0, 94, (0, 94))
            df = df[(df['SHOT_DISTANCE'] >= shotdistance_min) & (df['SHOT_DISTANCE'] <= shotdistance_max)]
        players = df['PLAYER_NAME'].unique()
        Players = st.sidebar.toggle('Players')
        if Players == 1:
            playrs = st.sidebar.multiselect('',players)
            df = df[df['PLAYER_NAME'].isin(playrs)]

        plays = []
        for index, row in df.iterrows():
            # Concatenate home team and away team names for the current row
            eventnum = row['GAME_EVENT_ID']
            d = row['PLAYER_NAME'] + ' ' + row['SHOT_RESULT'] + ' ' + str(row['SHOT_DISTANCE']) + ' ft' + ' '  + row['ACTION_TYPE'] + ': ' + row['SHOT_TYPE'] 
            if row['PERIOD'] == 1:
                q = '1st'
            elif row['PERIOD'] == 2:
                q = '2nd'
            elif row['PERIOD'] == 3:
                q = '3rd'
            elif row['PERIOD'] == 4:
                q = '4th'
            if row['SECONDS_REMAINING'] < 10:
                row['SECONDS_REMAINING'] = '0' + str(row['SECONDS_REMAINING'])
            t = str(row['MINUTES_REMAINING']) + ':' + str(row['SECONDS_REMAINING'])
            desc = f"{row['HTM']} vs {row['VTM']} | {q} Quarter - {t} | {d} | {row['GAME_ID']} | {row['PLAYER_ID']} | {eventnum}"
            plays.append(desc)

        length = len(df)
        plays = st.selectbox(f'Select Play ({length})', [''] + plays)
        if plays != '': 
            # Split the description string by ' - ' to separate components
            components = plays.split(' | ')

        # Extract the playid from the last component
            playid = components[-1]
            playerid = components[-2]
            id = components[-3]
            shot = components[2]
            timeq = components[1]
            teams = components[0]

            
            teams2 = components[0].split(' vs ')
            hometeam = teams2[0]
            awayteam = teams2[1]
            homeabbrev = hometeam.lower()
            awayabbrev = awayteam.lower()
            st.markdown(f"<h1 style='text-align: center; font-size: 30px;'>{teams}</h1>", unsafe_allow_html=True)

            col1, col2,col3 = st.columns(3)
            with col1:
                display_team_image(homeabbrev,300)
            with col2:
                display_player_image(player_id=playerid,width2=350,caption2='')
            with col3:
                display_team_image(awayabbrev,300)
            st.subheader('')

            headers = {
            'Host': 'stats.nba.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true',
            'Connection': 'keep-alive',
            'Referer': 'https://stats.nba.com/',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }
            event_id = playid
            game_id = id
            df = df[df['GAME_ID'] == game_id]
            df = df[(df['GAME_EVENT_ID'] == int(event_id))]
            shot_data = df
            text_all = (
                shot_data['ACTION_TYPE'] +  # Assuming 'description' is already a string
                ' (' + shot_data['SHOT_DISTANCE'].astype(str) + ' ft)'  # Convert shotDistance to string and concatenate
            )

            # Define the hover template
            hover_template = (
                "<b></b>%{customdata[0]}<br>"
            )

            # Assign the processed data back to shot_data if needed
            shot_data['desc'] = shot_data['ACTION_TYPE']
            shot_data['dist'] = shot_data['SHOT_DISTANCE'].astype(str) + ' ft'



            url = 'https://stats.nba.com/stats/videoeventsasset?GameEventID={}&GameID={}'.format(
                        event_id, game_id)
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                json = r.json()
                video_urls = json['resultSets']['Meta']['videoUrls']
                playlist = json['resultSets']['playlist']
                video_event = {'video': video_urls[0]['lurl'], 'desc': playlist[0]['dsc']}
                video = video_urls[0]['lurl']
                make_trace = go.Scatter(
                    x=(shot_data[shot_data["SHOT_MADE_FLAG"] == 1]["LOC_X"]),
                    y=shot_data[shot_data["SHOT_MADE_FLAG"] == 1]["LOC_Y"],
                    mode='markers',
                    marker=dict(color='rgba(0, 128, 0, 0.6)', size=13),
                    name='Made Shot ✅',
                    customdata=shot_data[shot_data["SHOT_MADE_FLAG"] == 1][['desc', 'dist']],  # Use customdata for makes only
                    hoverinfo='text',  # Set hoverinfo to text
                    hovertemplate=hover_template
                )
                # Create trace for misses
                miss_trace = go.Scatter(
                    x=(shot_data[shot_data["SHOT_MADE_FLAG"] == 0]["LOC_X"]),
                    y=shot_data[shot_data["SHOT_MADE_FLAG"] == 0]["LOC_Y"],
                    mode='markers',
                    marker=dict(symbol='x', color='rgba(255, 0, 0, 0.6)', size=13),
                    name='Missed Shot ❌',
                    customdata=shot_data[shot_data["SHOT_MADE_FLAG"] == 0][['desc', 'dist']],  # Use customdata for makes only
                    hoverinfo='text',  # Set hoverinfo to text
                    hovertemplate=hover_template
                )
                layout = go.Layout(
                hovermode='closest',
                xaxis=dict(showline=False, showticklabels=False, showgrid=False, range=[-260, 260]),
                yaxis=dict(showline=False, showticklabels=False, showgrid=False, range=[250, 115]),
                plot_bgcolor='#D2B48C',  # Set background color to the desired color

                width=390,  # Set the width of the background
                height=360,  # Set the height of the background
                autosize=False,
                legend=dict(x=0.98, y=1, xanchor='right', yanchor='top', bgcolor='rgba(0,0,0,0)',font=dict(color='black'), bordercolor='black', borderwidth=0),
                margin=dict(l=0, r=0, t=0, b=0)# Customize legend
                )

                # Create figure

                fig = go.Figure()
                draw_plotly_court(fig)
                fig.update_layout(layout)
                fig.add_trace(make_trace)
                fig.add_trace(miss_trace)

                fig.update_yaxes(scaleanchor='x', scaleratio=1)
                col1, col2= st.columns(2)
                with col1:
                    st.video(video)
                st.subheader(timeq + ' | ' + shot)
                with col2:
                    st.plotly_chart(fig)
                
            else:
                st.error('No Video Found')

















    else:
        typeszn = st.checkbox('Playoffs?')
        if typeszn:
            type = 'Playoffs'
        else:
            type = 'Regular Season'
        # Initialize the TeamGameLogs endpoint
        team_game_logs = TeamGameLogs(season_nullable=season,season_type_nullable=type)

        # Make the API request
        team_game_logs_data = team_game_logs.get_data_frames()
        team_game_logs_data[0] = team_game_logs_data[0].drop_duplicates(subset=['GAME_ID'])
        # st.write(team_game_logs_data[0].columns)
        # ids = team_game_logs_data[0]['GAME_ID']
        # id = st.selectbox('Select a game', ids)
        games = []
        for index, row in team_game_logs_data[0].iterrows():
            # Concatenate home team and away team names for the current row
            ddate2 = row['GAME_DATE']
            parsed_date2 = datetime.strptime(ddate2, "%Y-%m-%dT%H:%M:%S")
            # Format the datetime object into the desired string format
            formatted_date2 = parsed_date2.strftime("%m/%d/%Y")
            game = f"{row['MATCHUP']} | {formatted_date2} | {row['GAME_ID']}"
            # Append the concatenated string to the games list
            games.append(game)# Create a selectbox in Streamlit
        games = st.selectbox('Select game', [''] + games)
        if games:
            parts = games.split('|')


            # Extract the last element (which contains the number) and strip any extra whitespace
            id = parts[-1].strip()
            matchup = parts[-3].strip()
            hometeam = ''
            awayteam = ''

            if '@' in matchup:
                teams = matchup.split(' @ ')
                awayteam = teams[0]
                hometeam = teams[1]
            elif 'vs' in matchup:
                teams = matchup.split(' vs. ')
                hometeam = teams[0]
                awayteam = teams[1]
            if id:
                
                # plz = fetch_play_by_play_data(id)
                # Initialize PlayByPlay endpoint with the selected game ID
                response = ShotChartDetail(
                    game_id_nullable= id,
                    team_id=0,
                    player_id=0,
                    context_measure_simple = 'FGA', #<-- Default is 'PTS' and will only return made shots, but we want all shot attempts
                )
                content = json.loads(response.get_json())

                results = content['resultSets'][0]
                headers = results['headers']
                rows = results['rowSet']
                fevents_df = pd.DataFrame(rows, columns=headers) #<-- add the columns parameter
            
            # Check if data is successfully fetched
                    
                
                
        
                # play_by_play = PlayByPlayV3(game_id=id)
                # play_by_play_data = play_by_play.get_data_frames()
                # events_df = play_by_play_data[0]
                # finalplaybyplay = ShotChartDetail(game_id_nullable=id,player_id=0,team_id=0)
                # finalplaybyplaydata = finalplaybyplay.get_data_frames()
                # finalevents = finalplaybyplaydata[0] 
                fevents_df['SHOT_RESULT'] = fevents_df['EVENT_TYPE'].apply(lambda x: x.split()[0])
                

                shots = fevents_df['ACTION_TYPE'].unique()
                Makes = st.sidebar.toggle('Make/Miss')
                if Makes == 1:
                    makes = st.sidebar.selectbox('', ['Made', 'Missed'])
                    if makes == 'Made':
                        fmakes = 1
                        fevents_df = fevents_df[fevents_df['SHOT_MADE_FLAG'] == fmakes]
                    elif makes == 'Missed':
                        fmakes = 0
                        fevents_df = fevents_df[fevents_df['SHOT_MADE_FLAG'] == fmakes]
                Shottype = st.sidebar.toggle('Shot Type')
                if Shottype == 1:
                    shottype = st.sidebar.multiselect('', shots)
                    fevents_df = fevents_df[fevents_df['ACTION_TYPE'].isin(shottype)]
                Points = st.sidebar.toggle('Points')
                allpoints = fevents_df['SHOT_TYPE'].unique()
                if Points == 1:
                    points = st.sidebar.selectbox('', allpoints)
                    fevents_df = fevents_df[fevents_df['SHOT_TYPE'] == points]
                Quarter = st.sidebar.toggle('Quarter')
                if Quarter == 1:
                    fevents_df['QUARTER'] = fevents_df['PERIOD']
                    quarts = fevents_df['QUARTER'].unique()
                    quart = st.sidebar.multiselect('',quarts)
                    fevents_df = fevents_df[fevents_df['QUARTER'].isin(quart)]
                Time = st.sidebar.toggle('Time')
                if Time == 1:
                    timemin, timemax = st.sidebar.slider("Time Remaining (Minutes)", 0, 15, (0, 15))
                    fevents_df = fevents_df[(fevents_df['MINUTES_REMAINING'] >= timemin) & (fevents_df['MINUTES_REMAINING'] <= timemax)]
                Shotdist = st.sidebar.toggle('Shot Distance')
                if Shotdist == 1:
                    shotdistance_min, shotdistance_max = st.sidebar.slider("Shot Distance", 0, 94, (0, 94))
                    fevents_df = fevents_df[(fevents_df['SHOT_DISTANCE'] >= shotdistance_min) & (fevents_df['SHOT_DISTANCE'] <= shotdistance_max)]
                players = fevents_df['PLAYER_NAME'].unique()
                Players = st.sidebar.toggle('Players')
                if Players == 1:
                    playrs = st.sidebar.multiselect('',players)
                    fevents_df = fevents_df[fevents_df['PLAYER_NAME'].isin(playrs)]

                
                plays = []
                for index, row in fevents_df.iterrows():
                    # Concatenate home team and away team names for the current row
                    eventnum = row['GAME_EVENT_ID']
                    if row['SECONDS_REMAINING'] < 10:
                        row['SECONDS_REMAINING'] = '0' + str(row['SECONDS_REMAINING'])
                    d = row['PLAYER_NAME'] + ' ' + row['SHOT_RESULT'] + ' ' + str(row['SHOT_DISTANCE']) + ' ft' + ' '  + row['ACTION_TYPE'] + ': ' + row['SHOT_TYPE'] 
                    if row['PERIOD'] == 1:
                        q = '1st'
                    elif row['PERIOD'] == 2:
                        q = '2nd'
                    elif row['PERIOD'] == 3:
                        q = '3rd'
                    elif row['PERIOD'] == 4:
                        q = '4th'
                    t = str(row['MINUTES_REMAINING']) + ':' + str(row['SECONDS_REMAINING'])
                    desc = f" {q} Quarter - {t} | {d} | {row['PLAYER_ID']} | {eventnum}"
                    plays.append(desc)

                length = len(fevents_df)
                plays = st.selectbox(f'Select Play ({length})', [''] + plays)
                if plays != '': 
                    # Split the description string by ' - ' to separate components
                    components = plays.split(' | ')

                # Extract the playid from the last component
                    playid = components[-1]
                    playerid = components[-2]
                    shot = components[1]
                    timeq = components[0]
                    
                
                    
                        
                    homeabbrev = map_team_to_abbreviation(hometeam)
                    awayabbrev = map_team_to_abbreviation(awayteam)
                    col1, col2,col3 = st.columns(3)
                    with col1:
                        display_team_image(homeabbrev,300)
                    with col2:
                        display_player_image(player_id=playerid,width2=350,caption2='')
                    with col3:
                        display_team_image(awayabbrev,300)
                    st.subheader('')

                    headers = {
                    'Host': 'stats.nba.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'x-nba-stats-origin': 'stats',
                    'x-nba-stats-token': 'true',
                    'Connection': 'keep-alive',
                    'Referer': 'https://stats.nba.com/',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache'
                }
                    event_id = playid
                    game_id = id
                    events_df = events_df[events_df['actionNumber'] == int(event_id)]
                    shot_data = events_df
                    shot_data = events_df
                    text_all = (
                        shot_data['description'] +  # Assuming 'description' is already a string
                        ' (' + shot_data['shotDistance'].astype(str) + ' ft)'  # Convert shotDistance to string and concatenate
                    )

                    # Define the hover template
                    hover_template = (
                        "<b></b>%{customdata[0]}<br>"
                    )

                    # Assign the processed data back to shot_data if needed
                    shot_data['desc'] = shot_data['description']
                    shot_data['dist'] = shot_data['shotDistance'].astype(str) + ' ft'



                    url = 'https://stats.nba.com/stats/videoeventsasset?GameEventID={}&GameID={}'.format(
                                event_id, game_id)
                    r = requests.get(url, headers=headers)
                    if r.status_code == 200:
                        json = r.json()
                        video_urls = json['resultSets']['Meta']['videoUrls']
                        playlist = json['resultSets']['playlist']
                        video_event = {'video': video_urls[0]['lurl'], 'desc': playlist[0]['dsc']}
                        video = video_urls[0]['lurl']
                        make_trace = go.Scatter(
                            x=(shot_data[shot_data["shotResult"] == 'Made']["xLegacy"]),
                            y=shot_data[shot_data["shotResult"] == 'Made']["yLegacy"],
                            mode='markers',
                            marker=dict(color='rgba(0, 128, 0, 0.6)', size=13),
                            name='Made Shot ✅',
                            customdata=shot_data[shot_data["shotResult"] == 'Made'][['desc', 'dist']],  # Use customdata for makes only
                            hoverinfo='text',  # Set hoverinfo to text
                            hovertemplate=hover_template
                        )
                        # Create trace for misses
                        miss_trace = go.Scatter(
                            x=(shot_data[shot_data["shotResult"] == 'Missed']["xLegacy"]),
                            y=shot_data[shot_data["shotResult"] == 'Missed']["yLegacy"],
                            mode='markers',
                            marker=dict(symbol='x', color='rgba(255, 0, 0, 0.6)', size=13),
                            name='Missed Shot ❌',
                            customdata=shot_data[shot_data["shotResult"] == 'Missed'][['desc', 'dist']],  # Use customdata for makes only
                            hoverinfo='text',  # Set hoverinfo to text
                            hovertemplate=hover_template
                        )
                        layout = go.Layout(
                        hovermode='closest',
                        xaxis=dict(showline=False, showticklabels=False, showgrid=False, range=[-260, 260]),
                        yaxis=dict(showline=False, showticklabels=False, showgrid=False, range=[250, 115]),
                        plot_bgcolor='#D2B48C',  # Set background color to the desired color

                        width=390,  # Set the width of the background
                        height=360,  # Set the height of the background
                        autosize=False,
                        legend=dict(x=0.98, y=1, xanchor='right', yanchor='top', bgcolor='rgba(0,0,0,0)',font=dict(color='black'), bordercolor='black', borderwidth=0),
                        margin=dict(l=0, r=0, t=0, b=0)# Customize legend
                        )

                        # Create figure

                        fig = go.Figure()
                        draw_plotly_court(fig)
                        fig.update_layout(layout)
                        fig.add_trace(make_trace)
                        fig.add_trace(miss_trace)

                        fig.update_yaxes(scaleanchor='x', scaleratio=1)
                        col1, col2= st.columns(2)
                        with col1:
                            st.video(video)
                        st.markdown(f"<h1 style='text-align: center; font-size: 30px;'>{timeq} | {shot}</h1>", unsafe_allow_html=True)
                        # st.subheader(timeq + ' | ' + shot)
                        with col2:
                            st.plotly_chart(fig)
                        
                    else:
                        st.error('No Video Found')
  
