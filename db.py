import sqlite3
from sqlite3 import Error

import pandas as pd

file = 'scores.db'


def create_table():
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        c.execute(""" CREATE TABLE IF NOT EXISTS scores (
        player_name TEXT NOT NULL,
        location TEXT NOT NULL,
        score INT NOT NULL,
        attempted INT NOT NULL,
        pct REAL NOT NULL );""")
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()


def add_scores(details):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    try:
        c.execute(""" 
                    INSERT INTO scores (player_name, location, score, attempted, pct) 
                    VALUES ('{0}', '{1}', {2}, {3}, {4}); """
                  .format(details['name'], details['location'], details['score'], details['attempted'], details['pct']))
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()


def get_scores():
    conn = sqlite3.connect(file)
    try:
        print(pd.read_sql_query('SELECT * from scores ORDER BY score DESC', conn, index_col='player_name'))
    except Error as e:
        print(e)
    finally:
        conn.close()
