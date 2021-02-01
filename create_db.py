import sqlite3 as sl
import pandas as pd 

con = sl.connect('data.db')

with con:
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rating INTEGER
        );
    """)

with con:
    con.execute("""
        CREATE TABLE MATCH (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            winner TEXT,
            loser TEXT,
            winner_rating INTEGER,
            loser_rating INTEGER
            

        );       
    """)

sql = 'INSERT INTO USER (name, rating) values(?, ?)'
data = [
    ('Jon Magnus', 1000),
    ('Henrik', 1000),
    ('Petter', 1000),
    ('Thomas', 1000),
    ('Benjamin', 1000)
]

with con:
    con.executemany(sql, data)



import Add_date
import Add_streak
import Add_starr 



con = sl.connect('data.db')
df_players2 = pd.read_sql_query("SELECT * FROM Match", con)
print(df_players2)

