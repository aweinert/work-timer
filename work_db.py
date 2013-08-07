#!/usr/bin/env python

import sqlite3

class Contract:
	def __init__(self, contract_id, name, start, end, hours):
		self.contract_id = contract_id
		self.name = name
		self.start = start
		self.end = end
		self.hours = hours

class Project:
	def __init__(self, project_id, name, contract):
		self.project_id = project_id
		self.name = name
		self.contract = contract

def initialize(db_connection):
	cursor = db_connection.cursor()

	cursor.execute("CREATE TABLE Contracts (ContractId INTEGER PRIMARY KEY, Name TEXT, Start DATE, End DATE, Hours INTEGER)")
	cursor.execute("CREATE TABLE Projects (ProjectId INTEGER PRIMARY KEY, Name TEXT, ContractId INTEGER REFERENCES Contracts(ContractId))")
	cursor.execute("CREATE TABLE Categories (CategoryId INTEGER PRIMARY KEY, Name TEXT)")
	cursor.execute("CREATE TABLE Times (TimeId INTEGER PRIMARY KEY, ProjectId INTEGER REFERENCES Projects(ProjectId), Start DATETIME, End DATETIME, Description TEXT)")

	db_connection.commit()

def add_contract(db_connection, name, start, end, hours):
	db_cursor = db_connection.cursor()

	query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
	db_cursor.execute(query, (name, start, end, hours))
	contract_id = db_cursor.lastrowid

	db_connection.commit()

	contract = Contract(contract_id, name, start, end, hours)

	return contract

def add_project(db_connection, name, contract):
	db_cursor = db_connection.cursor()

	query = "INSERT INTO Projects (Name, ContractId) VALUES (?, ?)"
	db_cursor.execute(query, name, contract.contract_id)
	project_id = db_cursor.lastrowid

	db_connection.commit()

	project = Project(project_id, name, contract.contract_id)

	return project

db_path = "work.db"
db_connection = sqlite3.connect(db_path)

contract = add_contract(db_connection, "AlgoSyn", "2013-08-01", "2013-11-31", 10)
