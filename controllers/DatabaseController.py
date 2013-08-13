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
		
	def delete(self, obj):
		obj_id = self._get_id(obj)
		
		if obj_id in self._storage:
			del self._storage[obj_id]
		
	def retrieve_values(self):
		"""Returns all values in the cache as a list"""
		return self._storage.values()
	
	def retrieve_dict(self):
		"""Returns all currently cached values as a dictionary"""
		return self._storage.copy()

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
		
		self._contracts = self._create_and_populate_cache(self._contract_controller.retrieve_all_contracts,
														lambda contract: contract.contract_id,
														self._contract_controller.retrieve_contract_by_id)

		self._projects = self._create_and_populate_cache(self._project_controller.retrieve_all_projects,
														lambda project: project.project_id,
														self._project_controller.retrieve_project_by_id)

		self._categories = self._create_and_populate_cache(self._category_controller.retrieve_all_categories,
														lambda category: category.category_id,
														self._category_controller.retrieve_category_by_id)
		
		self._times = self._create_and_populate_cache(self._worktime_controller.retrieve_all_worktimes,
													lambda time: time.time_id,
													self._worktime_controller.retrieve_worktime_by_id)

	# CRUD-interface for contracts
	def create_contract(self, name, start, end, hours):
		contract = self._contract_controller.create_contract(name, start, end, hours)
		self._contracts.store(contract)
		return contract
	
	def retrieve_all_contracts(self):
		return self._contracts.retrieve_values()
	
	def retrieve_contract_by_id(self, contract_id):
		return self._contracts.retrieve(contract_id)
	
	def update_contract(self, contract):
		self._contract_controller.update_contract(contract)
	
	def delete_contract(self, contract):
		self._contract_controller.delete_contract(contract)
		self._contracts.delete(contract)

	# CRUD-interface for projects
	def create_project(self, name, contract):
		project = self._project_controller.create_project(name, contract)
		self._projects.store(project)
		return project
	
	def retrieve_all_projects(self):
		return self._projects.retrieve_values()
	
	def retrieve_project_by_id(self, project_id):
		return self._projects.retrieve(project_id)
	
	def update_project(self, project):
		self._project_controller.update_project(project)
	
	def delete_project(self, project):
		self._project_controller.delete_project(project)
		self._projects.delete(project)

	# CRUD-interface for categories
	def create_category(self, name):
		category = self._category_controller.create_category(name)
		self._categories.store(category)
		return category
	
	def retrieve_all_categories(self):
		return self._categories.retrieve_values()
	
	def retrieve_category_by_id(self, category_id):
		return self._categories.retrieve(category_id)
	
	def update_category(self, category):
		self._category_controller.update_category(category)
	
	def delete_category(self, category):
		self._category_controller.delete_category(category)
		self._categories.delete(category)
	
	# CRUD-interface for times
	def create_worktime(self, project, category, start, end, description):
		worktime = self._worktime_controller.create_worktime(project, category, start, end, description)
		self._times.store(worktime)
		return worktime
	
	def retrieve_all_worktimes(self):
		return self._times.retrieve_values()
	
	def retrieve_worktime_by_id(self, worktime_id):
		return self._times.retrieve(worktime_id)
	
	def update_worktime(self, worktime):
		self._worktime_controller.update_worktime(worktime)
	
	def delete_worktime(self, worktime):
		self._worktime_controller.delete_worktime(worktime)
		self._times.delete(worktime)
	
	def _create_and_populate_cache(self, creator_func, id_func, loader_func):
		return_value = CachedStore(id_func, loader_func)
		for obj in creator_func():
			return_value.store(obj)
			
		return return_value
				