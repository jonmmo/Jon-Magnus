from guizero import App, Text, PushButton, ListBox, Window, Combo
import sqlite3 as sl
import pandas as pd
#from utils import *

con = sl.connect('data.db')

def push_button():
    headline.value = "HEADLIINE"

def get_all_players():
    df = pd.read_sql_query('''SELECT * FROM USER''', con)
    return df

def update_rating(player):
    df = pd.read_sql_query("SELECT * FROM MATCH", con)
    print(df)
    player_opt_ranking_total = df.loc[df['winner'] == player, 'loser_rating'].sum() + df.loc[df['loser'] == player, 'winner_rating'].sum()

    player_win_loss = len(df[df['winner']==player]) - len(df[df['loser']==player])
    print(player_win_loss)
    total_games = len(df[df['winner']==player]) + len(df[df['loser']==player])
  
    new_rating = round((player_opt_ranking_total + 400 * player_win_loss)/total_games)
    print(new_rating)

    c = con.cursor()
    c.execute('''UPDATE USER SET rating = ? WHERE name = ?''', (new_rating, player))
    con.commit()

def get_rating(player):
    r = pd.read_sql_query('''SELECT rating FROM USER WHERE name = ?''', con, params=[player])
    rating = r['rating'].iloc[0]
    return rating

def update_data():
    data = get_all_players()
    data = data.sort_values('rating', ascending=False)
    print(data)
    players = []
    for i, row in data.iterrows():
        players.append(row['name'] + str(row['rating']))

    ranking.clear()
    for i in range(0, len(players)-1):
        ranking.insert(i, players[i]) 

def save_match(winner, loser):
    sql = 'INSERT INTO MATCH (winner, loser, winner_rating, loser_rating) values(?, ?, ?, ?)'
    winner_rating = int(get_rating(winner))
    loser_rating = int(get_rating(loser))
    data = [
        (winner, loser, winner_rating, loser_rating)
    ]
    with con:
        con.executemany(sql, data)
    update_rating(winner)
    update_rating(loser)
    register.hide()
    update_data()

def register_match(players):
    title = Text(register, text="Registrer resultat", size=20, font="Comic Sans MS", color="blue", grid=[0,0,4,1])
    label1 = Text(register, text="Vinner:",  grid=[0,1])
    winner = Combo(register, options=players, grid=[1,1])
    label1 = Text(register, text="Taper:",  grid=[2,1])
    loser = Combo(register, options=players, grid=[3,1])
    save_button = PushButton(register, command=lambda:save_match(winner.value, loser.value), text="Registrer resultat", grid=[0,3,2,1])
    register.show()
    
app = App("Pool system", layout = "grid")

# Get data
data = get_all_players()
data = data.sort_values('rating', ascending=False)
print(data)
players = []
for i, row in data.iterrows():
    players.append(row['name'] + str(row['rating']))

names = data.name
matches = pd.read_sql_query("SELECT * FROM MATCH", con)
print(matches)

# Register match window
register = Window(app, title="Registrer resultat", layout="grid")
register.hide()

# Main window
headline = Text(app, text="Pool system rating for C1.062", size=60, font="Comic Sans MS", color="blue", grid=[0,0,2,1], align="top")

ranking = ListBox(app, items=players, grid=[0,1])
last_games= ListBox(app, items=["Jon Magnus vs Henrik"], grid=[1,1])

register_button = PushButton(app, command=lambda:register_match(names), text="Registrer resultat", grid=[0,3,2,1])



app.display()