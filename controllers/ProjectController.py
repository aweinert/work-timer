from domain import *

class ProjectController:
	def __init__(self, db_connection, contract_controller):
		self._db_connection = db_connection
		self._contract_controller = contract_controller

	def add_project(self, name, contract):
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Projects (Name, ContractId) VALUES (?, ?)"
		db_cursor.execute(query, [name, contract.contract_id])
		project_id = db_cursor.lastrowid

		self._db_connection.commit()

		project = Project(project_id, name, contract)

		return project

	def get_all_projects_dict(self):
		contracts = self._contract_controller.get_all_contracts_dict()

		return_value = dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Projects"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			project = self._create_project_from_row(row, contracts)
			return_value[project.project_id] = project

		return return_value

	def _create_project_from_row(self, row, contract_dict):
		project_id = row[0]
		name = row[1]
		contract_id = row[2]

		project = Project(project_id, name, contract_dict[contract_id])
		return project
		
