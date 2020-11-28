from guizero import App, Text, PushButton, ListBox, Window, Combo, TextBox, Picture, CheckBox
import sqlite3 as sl
import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib import rc, dates as dts, figure as fig
from datetime import datetime
import numpy as np
import time 

con = sl.connect('data.db')


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


def save_match(winner, loser, perfect):
    sql = 'INSERT INTO MATCH (winner, loser, winner_rating, loser_rating, Date) values(?, ?, ?, ?, ?)'
    winner_rating = int(get_rating(winner))
    loser_rating = int(get_rating(loser))
    now =  (datetime.now())
    now_str = (now.strftime("%Y-%m-%d %H:%M:%S"))
    data = [
        (winner, loser, winner_rating, loser_rating,now_str)
    ]
    if perfect ==1:
        sql_string = 'UPDATE USER SET star = star+1 WHERE NAME = ?'
       
     
        with con:
            con.execute(sql_string,[winner])

   
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
    save_button = PushButton(register, command=lambda:save_match(winner.value, loser.value,checkbox.value), text="Registrer resultat", grid=[0,3,2,1])
    register.show()

    checkbox = CheckBox(register, text="7-0?", grid = [3,3])
    
        
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


def streak(names):
    streak_list=[]
    streak_value = "-" 
    df_players = pd.read_sql_query ('SELECT * FROM USER',con)



    for player in names:
        los_streak = 0
        win_streak = 0


        df = pd.read_sql_query("SELECT * FROM MATCH where winner=? or loser=?", con, params=[player,player])
        if len(df) == 0:
            streak_value="-"


        else:

             
            win_df = df[df.winner == player]
            los_df = df[df.loser == player] 
            if len(los_df) >0 and len(win_df) >0:
                last_los = max(los_df['id'])
                last_win = max(win_df['id'])

                if last_los > last_win:
                    los_streak = len(los_df[los_df['id'] > last_win ])
                    streak_value = "L" + str(los_streak)

                elif last_los < last_win:
                    win_streak = len(win_df[win_df['id'] > last_los ])
                    streak_value = "W" + str(win_streak)
            elif len(win_df)>0:
                win_streak = len(win_df)
                streak_value = "W" + str(win_streak)
            elif len(los_df)>0:
                los_streak = len(los_df)
                streak_value = "L" + str(los_streak)
        with con as c: 
            if win_streak > max(df_players[df_players.name == player].MAX_WIN_STREAK):
                c.execute('''UPDATE USER SET MAX_WIN_STREAK = ? WHERE name = ?''', (win_streak, player))
            elif los_streak > max(df_players[df_players.name == player].MAX_LOSE_STREAK):
                c.execute('''UPDATE USER SET MAX_LOSE_STREAK = ? WHERE name = ?''', (los_streak, player))

            
        streak_list.append(streak_value)
    return streak_list


def open_statistics():
    df = get_all_players()
    players = df['name'].tolist()
    title = Text(statistics, text="Statistikk", size=20, font="Comic Sans MS", color="blue", grid=[0,0,4,1])
    label1 = Text(statistics, text="Spiller 1",  grid=[0,1])
    one = Combo(statistics, options=players, grid=[1,1])
    label1 = Text(statistics, text="Spiller 2",  grid=[2,1])
    #players.append("ingen")
    two = Combo(statistics, options=players, grid=[3,1])
    save_button = PushButton(statistics, command=lambda:make_statistics(one.value, two.value), text="Se statistikk", grid=[4,1,2,1])
    statistics.show()


def make_statistics(player1, player2):
    p1_text = Text(statistics, text ="     "+player1+"     ", grid=[1,3,2,1])
    p2_text = Text(statistics, text ="     "+player2+"     ", grid=[3,3,2,1])
    df = pd.read_sql_query("SELECT * FROM MATCH", con)
    pdf = pd.read_sql_query("SELECT * FROM USER", con)
    p1_wins_df = df.loc[df['winner'] == player1]
    p1_loss_df = df.loc[df['loser'] == player1]
    p2_wins_df = df.loc[df['winner'] == player2]
    p2_loss_df = df.loc[df['loser'] == player2]
    p1_wins = len(p1_wins_df)
    p1_loss = len(p1_loss_df)
    p2_wins = len(p2_wins_df)
    p2_loss = len(p2_loss_df)
    p1_rating = int(pdf.loc[pdf['name'] == player1].rating)
    p2_rating = int(pdf.loc[pdf['name'] == player2].rating)
    p1_highest_rating = max(p1_wins_df['winner_rating'].max(), p1_loss_df['loser_rating'].max()) 
    p2_highest_rating = max(p2_wins_df['winner_rating'].max(), p2_loss_df['loser_rating'].max()) 
    p1_lowest_rating = min(p1_wins_df['winner_rating'].min(), p1_loss_df['loser_rating'].min()) 
    p2_lowest_rating = min(p2_wins_df['winner_rating'].min(), p2_loss_df['loser_rating'].min()) 
    p1_win_streak = int(pdf.loc[pdf['name'] == player1].MAX_WIN_STREAK)
    p2_win_streak = int(pdf.loc[pdf['name'] == player2].MAX_WIN_STREAK)
    p1_loss_streak = int(pdf.loc[pdf['name'] == player1].MAX_LOSE_STREAK)
    p2_loss_streak = int(pdf.loc[pdf['name'] == player2].MAX_LOSE_STREAK)
    internal_matches = p1_wins_df.loc[p1_wins_df['loser'] == player2] + p1_loss_df.loc[p1_loss_df['winner'] == player2]
    tot_matches = len(internal_matches)
    p1_int_wins = len(p1_wins_df.loc[p1_wins_df['loser'] == player2])
    p2_int_wins = len(p1_loss_df.loc[p1_loss_df['winner'] == player2])
    p1_perc = round(p1_int_wins*100/tot_matches,2)
    p2_perc = round(p2_int_wins*100/tot_matches,2)
    

    Text(statistics, text="Interne kamper", grid=[0,4])
    Text(statistics, text=str(tot_matches), grid=[2,4])

    Text(statistics, text="Kamper vunnet(%)", grid=[0,5])
    Text(statistics, text=str(p1_int_wins)+"("+str(p1_perc)+")", grid=[1,5])
    Text(statistics, text=str(p2_int_wins)+"("+str(p2_perc)+")", grid=[3,5])

    Text(statistics, text="Totale kamper", grid=[0,6])
    Text(statistics, text=str(p1_wins+p1_loss), grid=[1,6])
    Text(statistics, text=str(p2_wins+p2_loss), grid=[3,6])

    Text(statistics, text="Seiere", grid=[0,7])
    Text(statistics, text=str(p1_wins), grid=[1,7])
    Text(statistics, text=str(p2_wins), grid=[3,7])

    Text(statistics, text="Tap", grid=[0,8])
    Text(statistics, text=str(p1_loss), grid=[1,8])
    Text(statistics, text=str(p2_loss), grid=[3,8])

    Text(statistics, text="K/D", grid=[0,9])
    Text(statistics, text=str(round(p1_wins/p1_loss,2)), grid=[1,9])
    Text(statistics, text=str(round(p2_wins/p2_loss,2)), grid=[3,9])

    Text(statistics, text="Høyeste vinn-streak", grid=[0,10])
    Text(statistics, text=str(p1_win_streak), grid=[1,10])
    Text(statistics, text=str(p2_win_streak), grid=[3,10])

    Text(statistics, text="Høyeste tap-streak", grid=[0,1])
    Text(statistics, text=str(p1_loss_streak), grid=[1,11])
    Text(statistics, text=str(p2_loss_streak), grid=[3,11])

    Text(statistics, text="Rating", grid=[0,12])
    Text(statistics, text=str(p1_rating), grid=[1,12])
    Text(statistics, text=str(p2_rating), grid=[3,12])

    Text(statistics, text="Høyeste rating", grid=[0,13])
    Text(statistics, text=str(p1_highest_rating), grid=[1,13])
    Text(statistics, text=str(p2_highest_rating), grid=[3,13])

    Text(statistics, text="Laveste rating", grid=[0,14])
    Text(statistics, text=str(p1_lowest_rating), grid=[1,14])
    Text(statistics, text=str(p2_lowest_rating), grid=[3,14])


def make_GUI():
    # Get data
    data = get_all_players()
    data = data.sort_values('rating', ascending=False)
    data = data.reset_index(drop=True)
    names = data['name']
    star_num = data['STAR']

    name_list = names.tolist()
    streaks = streak(name_list)
    
    matches = pd.read_sql_query("SELECT * FROM MATCH", con)
    

    # Main window
    headline = Text(app, text="Pool-rankingsystem for kontor C1.062", size=60, font="Comic Sans MS", color="blue", grid=[0,0,6,1], align="top")
    rating = Text(app, text="Rankingliste", size = 20, grid=[1,1,3,1])
    navn = Text(app, text="Navn", grid =[2,2], size=14)
    score = Text(app, text="Score", grid=[3,2], size=14)
    
    
    for i, row in data.iterrows():
        stars=[]
        if star_num[i]>0:
           for a in range(star_num[i]):
               stars.append(chr(9733))
               
        else:
            stars =[""]
        stars=''.join(stars)
        text = str(i+1) + "."
        place = Text(app, text=text, grid=[1,i+3])
        name = Text(app, text=(
            '     '+ row['name']+stars+'   '), grid=[2,i+3])
        rank = Text(app, text=('     '+str(row['rating'])+" - Streak: "+streaks[i]+'     '), grid=[3,i+3])


    rating = Text(app, text="Siste kamper", size = 20, grid=[4,1,2,1])
    last_games = matches.tail(10)
    vinner = Text(app, text="Vinner", grid=[4,2], size=14)
    taper = Text(app, text="Taper", grid=[5,2], size=14)
    
    i = 0

    for j, row in last_games.iterrows():
        winner = Text(app, text=("      "+ row['winner']+ "      "), grid=[4,i+3], color="green")
        loser = Text(app, text=("      "+row['loser']+"      "), grid=[5,i+3], color="red")
        i += 1
   

    register_button = PushButton(app, command=lambda:register_match(names), text="Registrer resultat", grid=[4,17,2,1])
    statistics_button = PushButton(app, command=open_statistics, text="Se statistikk", grid=[2,17,2,1] )
    new_player_button = PushButton(app, command=new_player, text="Registrer ny spiller", grid=[0,17,2,1])

    # plot_types =['win/loss', 'History']
    # plt_type = Combo(app,options=plot_types, grid=[2,18,2,1])
    # plot_button = PushButton(app, command=make_plots(), text="Plott Win/Loss", grid=[3,18,2,1])
    
    make_plots()
    image = Picture(app,image="Plot.png",grid=[1,19,3,3])
    image2 = Picture(app,image="Historic_plot.png",grid=[4,19,3,3])

    # image_pie = Picture(app,image="pie.png",grid=[7,19,3,3])
    # exit_button = PushButton(app, command=exit, text="Exit Program", grid=[4,20,2,1])
 

def get_win_loss(names):

    df = pd.read_sql_query("SELECT * FROM MATCH", con)
    wins=[]
    losses=[]
    
    for x in names:
        wins.append( df[df['winner']==x].shape[0])
        losses.append( df[df['loser']==x].shape[0])
     
    return[wins,losses]


def get_historical_rating (names):
    df = pd.read_sql_query("SELECT * FROM MATCH", con)
    i=0
    rating_hist=[]
    now =  (datetime.now())

    date_hist=[]
    for x in names:
        rating=[]
        date =[]
        for i in range(0,df.shape[0]):
            if df.winner[i] ==x and not df.DATE[i] == '2020-11-02 12:00:00':
               rating.append(df.winner_rating[i])
               date.append(df.DATE[i])
            elif df.loser[i] == x and not df.DATE[i] == '2020-11-02 12:00:00':
                rating.append(df.loser_rating[i])
                date.append(df.DATE[i])
           
        rating.append(get_rating(x))
        date.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        dates = dts.datestr2num(date)
        rating_hist.append(rating)
        date_hist.append(dates)

    return[rating_hist,date_hist]
        

def make_plots():
    # print(plot_type)
    
    names=['Henrik', 'Jon Magnus','Thomas','Petter','Benjamin']
    
    [wins,losses]=get_win_loss(names)
    total = np.add(wins, losses) 


    r = list(range(0,len(names)))
   
    raw_data = {'greenBars': wins, 'orangeBars': losses,'blueBars': [0]*len(names)}
    df = pd.DataFrame(raw_data)
 
    # From raw value to percentage
    totals = [i+j+k for i,j,k in zip(df['greenBars'], df['orangeBars'], df['blueBars'])]
    greenBars = [i / j * 100 for i,j in zip(df['greenBars'], totals)]
    orangeBars = [i / j * 100 for i,j in zip(df['orangeBars'], totals)]
    blueBars = [i / j * 100 for i,j in zip(df['blueBars'], totals)]
    
    # plot
    barWidth = 0.85
    plt.figure(1)
    # Create green Bars
    plt.bar(r, greenBars, color='#b5ffb9', edgecolor='white', width=barWidth,)
    # Create orange Bars
    plt.bar(r, orangeBars, bottom=greenBars, color='#f9bc86', edgecolor='white', width=barWidth)
    # Create blue Bars
    # plt.bar(r, blueBars, bottom=[i+j for i,j in zip(greenBars, orangeBars)], color='#a3acff', edgecolor='white', width=barWidth)

   

    
    # Custom x axis
    plt.xticks(r, names)
    plt.xlabel("Spillere")
    plt.legend(['Wins', 'Losses'])

    # Save graphic
    plt.savefig("Plot.png", transparent = True)


    ## Historical plot 
    plt.figure(2)
    [rating_hist,date_list] = get_historical_rating(names)


    for rating, date in zip(rating_hist, date_list) :
        plt.plot_date(date,rating,'-')
        plt.legend(names,loc=2)


    
    plt.xticks(rotation=20)
  
    
    plt.savefig("Historic_plot",transparent = True) 
    plt.close()


app = App("Pool system", layout = "grid")
# Register match window
register = Window(app, title="Registrer resultat", layout="grid")
register.hide()

# New Player window
New_player_window = Window(app, title="Registrer resultat", layout="grid")
New_player_window.hide()

# Statistics window
statistics = Window(app, title="Statistikk", layout="grid")
statistics.hide()

make_GUI()


app.when_closed = exit 
app.display()
