#!/usr/bin/env python3

def init_bdd(url_name="sqlite://:memory:"):

	url = url_name.split("://")

	if url[0] == "sqlite":
		import sqlite3

		con = sqlite3.connect(url[1], check_same_thread=False)
		con.row_factory = sqlite3.Row


	init_table(con)

	con.commit()
	return con

	
def init_table(con):
	SQL = """
		CREATE TABLE IF NOT EXISTS history(
			 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			 idx INTEGER,
			 data FLOAT,
			 time TIMESTAMP
		);
		
		CREATE TABLE IF NOT EXISTS identifiant(
			 idx INTEGER PRIMARY KEY UNIQUE,
			 topic TEXT
		);
		
		CREATE TABLE IF NOT EXISTS event(
			 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			 ide INTEGER,
			 event_text TEXT,
			 time TIMESTAMP
		);
		
		CREATE TABLE IF NOT EXISTS dataset(
			 id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			 idd INTEGER,
			 type INTEGER,
			 ident INTEGER
		);
		
		CREATE TABLE IF NOT EXISTS dataset_info(
			 idd INTEGER PRIMARY KEY UNIQUE,
			 name TEXT
		);
		
	"""
	con.executescript(SQL)

def addHistoryData(con, idx, value):
	con.execute("""INSERT INTO history(idx, data, time) VALUES(?, ?, DATETIME("now") )""", (int(idx), float(value)))
	con.commit()
