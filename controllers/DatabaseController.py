import sqlite3

from ContractController import *
from CategoryController import *
from ProjectController import *
from WorktimeController import *

class DatabaseController:
	def __init__(self, db_path):
		self._db_connection = sqlite3.connect(db_path)
		cursor = self._db_connection.cursor()

		cursor.execute("CREATE TABLE IF NOT EXISTS Contracts (ContractId INTEGER PRIMARY KEY, Name TEXT, Start DATE, End DATE, Hours INTEGER)")
		cursor.execute("CREATE TABLE IF NOT EXISTS Projects (ProjectId INTEGER PRIMARY KEY, Name TEXT, ContractId INTEGER REFERENCES Contracts(ContractId))")
		cursor.execute("CREATE TABLE IF NOT EXISTS Categories (CategoryId INTEGER PRIMARY KEY, Name TEXT)")
		cursor.execute("CREATE TABLE IF NOT EXISTS Times (TimeId INTEGER PRIMARY KEY, ProjectId INTEGER REFERENCES Projects(ProjectId), CategoryId INTEGER REFERENCES Categories(CategoryId), Start DATETIME, End DATETIME, Description TEXT)")

		self._db_connection.commit()

		self.contract_controller = ContractController(self._db_connection)
		self.category_controller = CategoryController(self._db_connection)

		self.project_controller = ProjectController(self._db_connection, self.contract_controller)
		self.worktime_controller = WorktimeController(self._db_connection, self.project_controller, self.contract_controller)

