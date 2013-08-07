#!/usr/bin/env python

import sqlite3

def initialize(db_path = "work.db"):
	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("CREATE TABLE Contracts (ContractId INTEGER PRIMARY KEY, Name TEXT, Start DATE, End DATE, Hours INTEGER)")
	cursor.execute("CREATE TABLE Projects (ProjectId INTEGER PRIMARY KEY, Name TEXT, ContractId INTEGER REFERENCES Contracts(ContractId))")
	cursor.execute("CREATE TABLE Categories (CategoryId INTEGER PRIMARY KEY, Name TEXT)")
	cursor.execute("CREATE TABLE Times (TimeId INTEGER PRIMARY KEY, ProjectId INTEGER REFERENCES Projects(ProjectId), Start DATETIME, End DATETIME, Description TEXT)")

	connection.commit()

initialize()
