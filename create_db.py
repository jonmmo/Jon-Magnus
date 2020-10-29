import sqlite3 as sl

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
