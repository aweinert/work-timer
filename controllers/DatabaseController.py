import sqlite3

from ContractController import *
from CategoryController import *
from ProjectController import *
from WorktimeController import *

class CachedStore:
	"""Retrieves elements via some function and caches them after the first retrieval"""
	def __init__(self, id_func, loader_func):
		"""Initializes a cached store for a certain kind of objects
		
		Parameters
		----------
		id_func: Function that retrieves an unique id from an object given for storage
		loader_func: Function that loads an object based on its id, if it is not already cached"""

		self._storage = {}
		self._get_id = id_func
		self._load_by_id = loader_func
	
	def retrieve(self, object_id):
		if object_id in self._storage:
			return_value = self._storage[object_id]
		else:
			return_value = self._load_by_id(object_id)
			self._storage(return_value)
			
		return return_value
	
	def store(self, obj):
		object_id = self._get_id(obj)
		self._storage[object_id] = obj

class DatabaseController:
	def __init__(self, db_path):
		self._db_connection = sqlite3.connect(db_path)
		cursor = self._db_connection.cursor()

		cursor.execute("CREATE TABLE IF NOT EXISTS Contracts (ContractId INTEGER PRIMARY KEY, Name TEXT, Start DATE, End DATE, Hours INTEGER)")
		cursor.execute("CREATE TABLE IF NOT EXISTS Projects (ProjectId INTEGER PRIMARY KEY, Name TEXT, ContractId INTEGER REFERENCES Contracts(ContractId))")
		cursor.execute("CREATE TABLE IF NOT EXISTS Categories (CategoryId INTEGER PRIMARY KEY, Name TEXT)")
		cursor.execute("CREATE TABLE IF NOT EXISTS Times (TimeId INTEGER PRIMARY KEY, ProjectId INTEGER REFERENCES Projects(ProjectId), CategoryId INTEGER REFERENCES Categories(CategoryId), Start DATETIME, End DATETIME, Description TEXT)")

		self._db_connection.commit()

		self._contract_controller = ContractController(self._db_connection)
		self._category_controller = CategoryController(self._db_connection)

		self._project_controller = ProjectController(self._db_connection, self._contract_controller)
		self._worktime_controller = WorktimeController(self._db_connection, self._project_controller, self._contract_controller)

		# CRUD-interface for contracts
		def create_contract(self, name, start, end, hours):
			pass
		
		def retrieve_all_contracts(self):
			pass
		
		def retrieve_contract_by_id(self, contract_id):
			pass
		
		def update_contract(self, contract):
			pass
		
		def delete_contract(self, contract):
			pass

		# CRUD-interface for projects
		def create_project(self, name, contract):
			pass
		
		def retrieve_all_projects(self):
			pass
		
		def retrieve_project_by_id(self, project_id):
			pass
		
		def update_project(self, project):
			pass
		
		def delete_project(self, project):
			pass

		# CRUD-interface for categories
		def create_category(self, name):
			pass
		
		def retrieve_all_categories(self):
			pass
		
		def retrieve_category_by_id(self, category_id):
			pass
		
		def update_category(self, category):
			pass
		
		def delete_category(self, category):
			pass
		
		# CRUD-interface for times
		def create_worktime(self, name):
			pass
		
		def retrieve_all_worktimes(self):
			pass
		
		def retrieve_worktime_by_id(self, worktime_id):
			pass
		
		def update_worktime(self, worktime):
			pass
		
		def delete_worktime(self, worktime):
			pass