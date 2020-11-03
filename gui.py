from guizero import App, Text, PushButton, ListBox, Window, Combo, TextBox
import sqlite3 as sl
import pandas as pd
from datetime import datetime




#from utils import *

con = sl.connect('data.db')

def push_button():
    headline.value = "HEADLIINE"

def get_all_players():
    df = pd.read_sql_query('''SELECT * FROM USER''', con)
    return df

def update_rating(player):
    df = pd.read_sql_query("SELECT * FROM MATCH", con)
    player_opt_ranking_total = df.loc[df['winner'] == player, 'loser_rating'].sum() + df.loc[df['loser'] == player, 'winner_rating'].sum()

    player_win_loss = len(df[df['winner']==player]) - len(df[df['loser']==player])
    total_games = len(df[df['winner']==player]) + len(df[df['loser']==player])
  
    new_rating = round((player_opt_ranking_total + 400 * player_win_loss)/total_games)

    c = con.cursor()
    c.execute('''UPDATE USER SET rating = ? WHERE name = ?''', (new_rating, player))
    con.commit()

def get_rating(player):
    r = pd.read_sql_query('''SELECT rating FROM USER WHERE name = ?''', con, params=[player])
    rating = r['rating'].iloc[0]
    return rating

def save_match(winner, loser):
    sql = 'INSERT INTO MATCH (winner, loser, winner_rating, loser_rating, Date) values(?, ?, ?, ?, ?)'
    winner_rating = int(get_rating(winner))
    loser_rating = int(get_rating(loser))
    now =  (datetime.now())
    now_str = (now.strftime("%Y-%m-%d %H:%M:%S"))
    data = [
        (winner, loser, winner_rating, loser_rating,now_str)
    ]
    with con:
        con.executemany(sql, data)
    update_rating(winner)
    update_rating(loser)
    register.hide()
    make_GUI()

def register_match(players):
    title = Text(register, text="Registrer resultat", size=20, font="Comic Sans MS", color="blue", grid=[0,0,4,1])
    label1 = Text(register, text="Vinner:",  grid=[0,1])
    winner = Combo(register, options=players, grid=[1,1])
    label1 = Text(register, text="Taper:",  grid=[2,1])
    loser = Combo(register, options=players, grid=[3,1])
    save_button = PushButton(register, command=lambda:save_match(winner.value, loser.value), text="Registrer resultat", grid=[0,3,2,1])
    register.show()
    
app = App("Pool system", layout = "grid")

def write_player(new_player):
    sql = 'INSERT INTO USER (name, rating) values(?, ?)'
    data = [
        (new_player, 1000)
        ]
    with con:
        con.executemany(sql, data)

    New_player_window.hide()
    make_GUI()

def new_player():
    title = Text(New_player_window, text="New Player", size=20, font="Comic Sans MS", color="blue", grid=[0,0,4,1])
    label1 = Text(New_player_window, text="New player:",  grid=[0,1])
    player = TextBox(New_player_window,grid=[0,2])
    save_button = PushButton(New_player_window, command=lambda:write_player(player.value ), text="Registrer ny spiller", grid=[0,3,2,1])
    New_player_window.show()

def make_GUI():
    # Get data
    data = get_all_players()
    data = data.sort_values('rating', ascending=False)
    data = data.reset_index(drop=True)
    names = data['name']

    matches = pd.read_sql_query("SELECT * FROM MATCH", con)
    

    # Main window
    headline = Text(app, text="Pool-rankingsystem for kontor C1.062", size=60, font="Comic Sans MS", color="blue", grid=[0,0,6,1], align="top")
    rating = Text(app, text="Rankingliste", size = 20, grid=[0,1,3,1])
    navn = Text(app, text="Navn", grid =[1,2], size=14)
    score = Text(app, text="Score", grid=[2,2], size=14)
    for i, row in data.iterrows():
        text = str(i+1) + "."
        place = Text(app, text=text, grid=[0,i+3])
        name = Text(app, text=row['name'], grid=[1,i+3])
        rank = Text(app, text=str(row['rating']), grid=[2,i+3])

    rating = Text(app, text="Siste kamper", size = 20, grid=[4,1,2,1])
    last_games = matches.tail(10)
    vinner = Text(app, text="Vinner", grid=[4,2], size=14)
    taper = Text(app, text="Taper", grid=[5,2], size=14)
    i = 0
    for j, row in last_games.iterrows():
        winner = Text(app, text=row['winner'], grid=[4,i+3], color="green")
        loser = Text(app, text=row['loser'], grid=[5,i+3], color="red")
        i += 1

    register_button = PushButton(app, command=lambda:register_match(names), text="Registrer resultat", grid=[4,17,2,1])

    new_player_button = PushButton(app, command=new_player, text="Registrer ny spiller", grid=[1,17,2,1])


# Register match window
register = Window(app, title="Registrer resultat", layout="grid")
register.hide()

# New Player window
New_player_window = Window(app, title="Registrer resultat", layout="grid")
New_player_window.hide()
make_GUI()

app.display()