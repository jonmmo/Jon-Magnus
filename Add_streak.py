import numpy as np 
import pandas as pd 
import sqlite3 as sl


con = sl.connect('data.db')

with con:
    con.execute("""
       ALTER TABLE USER  
           ADD MAX_WIN_STREAK INTEGER;
            
    """)



with con:
    con.execute("""
       ALTER TABLE USER 
           ADD MAX_LOSE_STREAK INTEGER;     
    """)


with con:
    con.execute("""
        UPDATE user
        SET MAX_WIN_STREAK
             = 0
    """)

with con:
    con.execute("""
        UPDATE user
        SET MAX_LOSE_STREAK
             = 0
    """)



# df_players = pd.read_sql_query("SELECT * FROM USER", con)

# names = df_players.name
# win_streak_list=[]
# lose_streak_list=[] 
# for player in names:
#     wins_streak = 0
#     loss_streak = 0
#     wins = 0
#     loss = 0
#     df = pd.read_sql_query("SELECT * FROM MATCH where winner=? or loser=?", con, params=[player,player])

#     for i in range(len(df)):
      
#         if df.winner[i] == player:
            
#             wins=wins+1 
#             if loss > loss_streak:
#                 loss_streak = loss
#             loss = 0
#         elif df.loser[i] == player :
#             loss=loss+1 
#             if wins > wins_streak:
#                 wins_streak = wins
#             wins = 0
#     with con:
#         con.execute("""
#             UPDATE USER
#             SET MAX_LOSE_STREAK = ?
#             WHERE NAME = ? 
#             """,(loss_streak,player))

#         con.execute("""
#             UPDATE USER
#             SET MAX_WIN_STREAK = ?
#             WHERE NAME = ?
#             """,(wins_streak,player))




df_players2 = pd.read_sql_query("SELECT * FROM USER", con)
print(df_players2)