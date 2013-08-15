from domain import Project

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

	def retrieve_all_projects(self, contract_dict):
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
		contract_dict = self._contract_controller.get_all_contracts_dict()

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