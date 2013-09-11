import domain

class CategoryController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_category(self, name):
		"""Stores a new category-domain object and returns it to the caller"""
		query = "INSERT INTO Categories (Name) VALUES (?)"
		category_id = self._db_connection.insert_single_row(query, [name])

		category = domain.Category(category_id, name)
		return category

	def retrieve_all_categories(self):
		"""Returns a list containing all categories in the database"""
		query = "SELECT * FROM Categories"

		rows = self._db_connection.retrieve_rows(query)
		return map(lambda row: self._create_category_from_row(row), rows)
	
	def retrieve_category_by_id(self, category_id):
		"""Returns the category with the given id, if it exists in the database.
		
		If there is no category with the given id, None is returned"""
		query = "SELECT * FROM Categories WHERE CategoryId = ?"

		row = self._db_connection.retrieve_single_row(query, [category_id])
		return self._create_category_from_row(row)
		
	def update_category(self, category):
		"""Writes the changes made in the given contract to the database"""
		query = "UPDATE Categories SET (name = ?) WHERE CategoryId = ?"
		self._db_connection.update_rows(query, [category.name, category.category_id])
		
	def delete_category(self, category):
		"""Removes the given category from the database.
		
		The given category is considered invalid after a call to this method"""
		query = "DELETE FROM Categories WHERE CategoryId = ?"
		self._db_connection.delete_rows(query, [category.category_id])

	def _create_category_from_row(self, row):
		"""Creates a category-domain object from the result of an SQL-query"""
		category_id = row[0]
		name = row[1]

		category = domain.Category(category_id, name)
		return category

class ContractController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_contract(self, name, start, end, hours):
		"""Writes a new domain-contract object and returns it to the caller"""
		query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
		contract_id = self._db_connection.create_single_row(query, [name, self._db_connection.python_datetime_to_sql(start), self._db_connection.python_datetime_to_sql(end), hours])

		contract = domain.Contract(contract_id, name, str(start), str(end), hours)

		return contract

	def retrieve_all_contracts(self):
		"""Returns a list containing all contracts in the database"""
		query = "SELECT * FROM Contracts"
		results = self._db_connection.retrieve_rows(query)
		return map(lambda row: self._create_contract_from_row(row), results)
	
	def retrieve_contract_by_id(self, contract_id):
		"""Returns the contract with the given id, if it exists in the database.
		
		If there is no contract with the given id, None is returned"""
		query = "SELECT * FROM Contracts WHERE ContractId = ?"
		return self._db_connection.retrieve_single_row(query)
	
	def update_contract(self, contract):
		query = "UPDATE Contracts SET (name = ?, start = ?, end = ?, hours = ?) WHERE contract_id = ?"
		self._db_connection.update_rows(query, [contract.name, self._db_connection.python_datetime_to_sql(contract.start), self._db_connection.python_datetime_to_sql(contract.end), contract.hours, contract.contract_id])
		
	def delete_contract(self, contract):
		"""Removes the given contract from the database.
		
		The given contract is considered invalid after a call to this method"""
		query = "DELETE FROM Contracts WHERE ContractId = ?"
		self._db_connection.delete_rows.execute(query, [contract.contract_id])
		
	def _create_contract_from_row(self, row):
		"""Creates a domain.Contract-object from a given row returned from the database"""
		contract_id = row[0]
		name = row[1]
		start = self._db_connection.sql_datetime_to_python(row[2]).date()
		end = self._db_connection.sql_datetime_to_python(row[3]).date()
		hours = row[4]

		contract = domain.Contract(contract_id, name, start, end, hours)
		return contract

class ProjectController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_project(self, name, contract):
		"""Stores a new project in the database and returns it to the caller"""
		query = "INSERT INTO Projects (Name, ContractId) VALUES (?, ?)"
		project_id = self._db_connection.create_single_row(query, [name, contract.contract_id])

		project = domain.Project(project_id, name, contract)

		return project

	def retrieve_all_projects(self):
		"""Returns a list containing all projects in the database"""
		query = "SELECT * FROM Projects"
		rows = self._db_connection.retrieve_rows(query)

		return map(lambda row: self._create_project_from_row(row), rows)
	
	def retrieve_project_by_id(self, project_id):
		"""Returns the project with the given id, if it exists in the database.
		
		If there is no project with the given id, None is returned"""
		query = "SELECT * FROM Projects WHERE ProjectId = ?"
		return self._db_connection.retrieve_single_row(query, [project_id])

	def update_project(self, project):
		"""Writes the changes made in the given project to the database"""
		query = "UPDATE Projects SET (name = ?, contract_id = ?) WHERE project_id = ?"
		self._db_connection.update_rows(query, [project.name, project.contract.contract_id, project.project_id])
		
	def delete_project(self, project):
		"""Removes the given project from the database.
		
		The given project is considered invalid after a call to this method"""
		query = "DELETE FROM Projects WHERE ProjectId = ?"
		self._db_connection.delete_rows(query, [project.project_id])

	def _create_project_from_row(self, row):
		"""Creates a domain.Project object from a row returned from a database query
		
		The contract_dict shall map contract_id to the contract with the given id.
		It may, for example, be obtained from some ContractController"""
		project_id = row[0]
		name = row[1]
		contract_id = row[2]
		contract = self._persistence_controller.retrieve_contract_by_id(contract_id)

		project = domain.Project(project_id, name, contract)
		return project

class WorktimeController:
	def __init__(self, db_connection, persistence_controller):
		self._db_connection = db_connection
		self._persistence_controller = persistence_controller

	def create_worktime(self, project, category, start, end, description):
		"""Writes a new domain-worktime object to the database and returns it to the caller"""
		query = "INSERT INTO Times (ProjectId, CategoryId, Start, End, Description) VALUES (?,?,?,?,?)"
		worktime_id = self._db_connection.create_single_row(query, [project.project_id, category.category_id, self._db_connection.python_datetime_to_sql(start), self._db_connection.python_datetime_to_sql(end), description])

		worktime = domain.Worktime(worktime_id, project.project_id, category.category_id, start, end, description)

		return worktime

	def retrieve_all_worktimes(self):
		"""Returns a list containing all worktimes in the database"""
		query = "SELECT * FROM Times"
		rows = self._db_connection.retrieve_rows(query)
		return map(lambda row: self._create_worktime_from_row(row), rows)

	def retrieve_worktime_by_id(self, worktime_id):
		"""Returns the worktime with the given id, if it exists in the database.
		
		If there is no worktime with the given id, None is returned"""
		query = "SELECT * FROM Times WHERE TimeId = ?"
		return self._db_connection.retrieve_single_row(query, [worktime_id])
	
	def update_worktime(self, time):
		"""Writes the changes made in the given worktime to the database"""
		query = "UPDATE Times SET ProjectId = ?, CategoryId = ?, Start = ?, End = ?, Description = ? WHERE TimeId = ?"
		self._db_connection.update_rows(query, [time.project.project_id, time.category.category_id, str(time.start), str(time.end), time.description, time.time_id])
		
	def delete_worktime(self, time):
		"""Removes the given worktime from the database.
		
		The given worktime is considered invalid after a call to this method"""
		query = "DELETE FROM Times WHERE TimeId = ?"
		self._db_connection.delete_rows(query, [time.time_id])

	def _create_worktime_from_row(self, row):
		"""Creates a domain.Worktime object from a row returned from a database query
		
		The dictionaries shall map the ids of their objects to the object with the given id.
		It may, for example, be obtained from some other Controller"""
		time_id = row[0]
		project_id = row[1]
		category_id = row[2]
		start = self._db_connection.sql_datetime_to_python(row[3])
		end = self._db_connection.sql_datetime_to_python(row[4])
		description = row[5]
		
		project = self._persistence_controller.retrieve_project_by_id(project_id)
		category = self._persistence_controller.retrieve_category_by_id(category_id)

		worktime = domain.Worktime(time_id, project, category, start, end, description)
		return worktime