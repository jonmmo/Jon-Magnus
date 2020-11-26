import numpy as np 
import pandas as pd 
import sqlite3 as sl


con = sl.connect('data.db')


with con:
    con.execute("""
       ALTER TABLE USER  
           ADD STAR INTEGER;     
    """)



with con:
    con.execute("""
        UPDATE USER
        SET 
            STAR = 0
    """)


df_players = pd.read_sql_query("SELECT * FROM USER", con)

df_match = pd.read_sql_query("SELECT * FROM MATCH", con)



