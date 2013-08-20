import dateutil.parser

from domain import *

class CategoryController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_category(self, name):
		"""Stores a new category-domain object and returns it to the caller"""
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Categories (Name) VALUES (?)"
		db_cursor.execute(query, [name])
		category_id = db_cursor.lastrowid

		self._db_connection.commit()

		category = Category(category_id, name)
		return category

	def retrieve_all_categories(self):
		"""Returns a list containing all categories in the database"""
		return_value = []
		
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Categories"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			category = self._create_category_from_row(row)
			return_value.append(category)

		return return_value
	
	def retrieve_category_by_id(self, category_id):
		"""Returns the category with the given id, if it exists in the database.
		
		If there is no category with the given id, None is returned"""
		db_cursor = self._db_connection.cursor()

		query = "SELECT * FROM Categories WHERE CategoryId = ?"
		db_cursor.execute(query, category_id)

		results = db_cursor.fetchall()
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_contract_from_row(results[0])
			
		return return_value
		
	def update_category(self, category):
		"""Writes the changes made in the given contract to the database"""
		db_cursor = self._db_connection.cursor()
		
		query = "UPDATE Categories SET (name = ?) WHERE CategoryId = ?"
		db_cursor.execute(query, category.name, category.category_id)
		
		self._db_connection.commit()
		
	def delete_category(self, category):
		"""Removes the given category from the database.
		
		The given category is considered invalid after a call to this method"""
		db_cursor = self._db_connection.cursor()
		
		query = "DELETE FROM Categories WHERE CategoryId = ?"
		db_cursor.execute(query, category.category_id)
		
		self._db_connection.commit()

	def _create_category_from_row(self, row):
		"""Creates a category-domain object from the result of an SQL-query"""
		category_id = row[0]
		name = row[1]

		category = Category(category_id, name)
		return category

class ContractController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_contract(self, name, start, end, hours):
		"""Writes a new domain-contract object and returns it to the caller"""
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
		db_cursor.execute(query, [name, self._python_datetime_to_sql(start), self._python_datetime_to_sql(end), hours])
		contract_id = db_cursor.lastrowid

		self._db_connection.commit()

		contract = Contract(contract_id, name, str(start), str(end), hours)

		return contract

	def retrieve_all_contracts(self):
		"""Returns a list containing all contracts in the database"""
		# Initialize return_value
		return_value = []

		# Actually query database
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Contracts"
		db_cursor.execute(query)

		# Create objects from returned rows
		for row in db_cursor.fetchall():
			contract = self._create_contract_from_row(row)
			return_value.append(contract)

		return return_value
	
	def retrieve_contract_by_id(self, contract_id):
		"""Returns the contract with the given id, if it exists in the database.
		
		If there is no contract with the given id, None is returned"""
		db_cursor = self._db_connection.cursor()

		query = "SELECT * FROM Contracts WHERE ContractId = ?"
		db_cursor.execute(query, contract_id)
		
		results = db_cursor.fetchall()
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_contract_from_row(results[0])

		return return_value
	
	def update_contract(self, contract):
		"""Writes the changes made in the given contract to the database"""
		db_cursor = self._db_connection.cursor()
		
		query = "UPDATE Contracts SET (name = ?, start = ?, end = ?, hours = ?) WHERE contract_id = ?"
		db_cursor.execute(query, contract.name, self._python_datetime_to_sql(contract.start), self._python_datetime_to_sql(contract.end), contract.hours, contract.contract_id)
		
		self._db_connection.commit()
		
	def delete_contract(self, contract):
		"""Removes the given contract from the database.
		
		The given contract is considered invalid after a call to this method"""
		db_cursor = self._db_connection.cursor()
		
		query = "DELETE FROM Contracts WHERE ContractId = ?"
		db_cursor.execute(query, contract.contract_id)
		
		self._db_connection.commit()
		
	def _create_contract_from_row(self, row):
		"""Creates a domain.Contract-object from a given row returned from the database"""
		contract_id = row[0]
		name = row[1]
		start = self._sql_datetime_to_python(row[2]).date()
		end = self._sql_datetime_to_python(row[3]).date()
		hours = row[4]

		contract = Contract(contract_id, name, start, end, hours)
		return contract

	def _python_datetime_to_sql(self, datetime):
		"""Returns a parameter fit for passing to sqlite3.cursor.execute(query,...)
		
		If datetime is None, it returns None. Otherwise it returns a string-representation
		of the datetime-object."""
		
		if datetime <> None:
			return str(datetime)
		else:
			return None
		
	def _sql_datetime_to_python(self, sql_entry):
		"""Creates a python object from an entry returned from a database
		
		If the returned entry is None, None is returned. Otherwise, the entry
		is parsed and encapsulated in a datetime-object"""
		
		if sql_entry <> None:
			return dateutil.parser.parse(sql_entry)
		else:
			return None

class ProjectController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_project(self, name, contract):
		"""Stores a new project in the database and returns it to the caller"""
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Projects (Name, ContractId) VALUES (?, ?)"
		db_cursor.execute(query, [name, contract.contract_id])
		project_id = db_cursor.lastrowid

		self._db_connection.commit()

		project = Project(project_id, name, contract)

		return project

	def retrieve_all_projects(self):
		"""Returns a list containing all projects in the database"""
		# Initialize return value
		return_value = []

		# Query database
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Projects"
		db_cursor.execute(query)

		# Process the retrieved rows and create business objects from them
		for row in db_cursor.fetchall():
			project = self._create_project_from_row(row)
			return_value.append(project)

		return return_value
	
	def retrieve_project_by_id(self, project_id):
		"""Returns the project with the given id, if it exists in the database.
		
		If there is no project with the given id, None is returned"""
		db_cursor = self._db_connection.cursor()

		query = "SELECT * FROM Projects WHERE ProjectId = ?"
		db_cursor.execute(query, project_id)
		
		results = db_cursor.fetchall()
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_project_from_row(results[0])

		return return_value

	def update_project(self, project):
		"""Writes the changes made in the given project to the database"""
		db_cursor = self._db_connection.cursor()
		
		query = "UPDATE Projects SET (name = ?, contract_id = ?) WHERE project_id = ?"
		db_cursor.execute(query, project.name, project.contract.contract_id, project.project_id)
		
	def delete_project(self, project):
		"""Removes the given project from the database.
		
		The given project is considered invalid after a call to this method"""
		db_cursor = self._db_connection.cursor()
		
		query = "DELETE FROM Projects WHERE ProjectId = ?"
		db_cursor.execute(query, project.project_id)
		
		self._db_connection.commit()

	def _create_project_from_row(self, row):
		"""Creates a domain.Project object from a row returned from a database query
		
		The contract_dict shall map contract_id to the contract with the given id.
		It may, for example, be obtained from some ContractController"""
		project_id = row[0]
		name = row[1]
		contract_id = row[2]
		contract = self._persistence_controller.retrieve_contract_by_id(contract_id)

		project = Project(project_id, name, contract)
		return project

class WorktimeController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_worktime(self, project, category, start, end, description):
		"""Writes a new domain-worktime object to the database and returns it to the caller"""
		db_cursor = self._db_connection.cursor()

		if start <> None:
			start_param = str(start)
		else:
			start_param = None

		if end <> None:
			end_param = str(end)
		else:
			end_param = None

		query = "INSERT INTO Times (ProjectId, CategoryId, Start, End, Description) VALUES (?,?,?,?,?)"
		db_cursor.execute(query, [project.project_id, category.category_id, start_param, end_param, description])
		worktime_id = db_cursor.lastrowid

		self._db_connection.commit()

		worktime = Worktime(worktime_id, project.project_id, category.category_id, start, end, description)

		return worktime

	def retrieve_all_worktimes(self):
		"""Returns a list containing all worktimes in the database"""
		return_value = []

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Times"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			worktime = self._create_worktime_from_row(row)
			return_value.append(worktime)

		return return_value

	def retrieve_worktime_by_id(self, worktime_id):
		"""Returns the worktime with the given id, if it exists in the database.
		
		If there is no worktime with the given id, None is returned"""
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Times WHERE TimeId = ?"
		db_cursor.execute(query, worktime_id)

		results = db_cursor.fetchall()
		
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_worktime_from_row(results[0])

		return return_value
	
	def update_worktime(self, time):
		"""Writes the changes made in the given worktime to the database"""

		db_cursor = self._db_connection.cursor()
		query = "UPDATE Times SET ProjectId = ?, CategoryId = ?, Start = ?, End = ?, Description = ? WHERE TimeId = ?"
		db_cursor.execute(query, [time.project.project_id, time.category.category_id, str(time.start), str(time.end), time.description, time.time_id])
		self._db_connection.commit()
		
	def delete_worktime(self, time):
		"""Removes the given worktime from the database.
		
		The given worktime is considered invalid after a call to this method"""
		db_cursor = self._db_connection.cursor()
		
		query = "DELETE FROM Times WHERE TimeId = ?"
		db_cursor.execute(query, time.time_id)
		
		self._db_connection.commit()
		

	def _create_worktime_from_row(self, row):
		"""Creates a domain.Worktime object from a row returned from a database query
		
		The dictionaries shall map the ids of their objects to the object with the given id.
		It may, for example, be obtained from some other Controller"""
		time_id = row[0]
		project_id = row[1]
		category_id = row[2]

		if row[3] <> None:
			start = dateutil.parser.parse(row[3])
		else:
			start = None

		if row[4] <> None:
			end = dateutil.parser.parse(row[4])
		else:
			end = None

		description = row[5]
		
		project = self._persistence_controller.retrieve_project_by_id(project_id)
		category = self._persistence_controller.retrieve_category_by_id(category_id)

		worktime = Worktime(time_id, project, category, start, end, description)
		return worktime