from domain import *

class ProjectController:
	def __init__(self, db_connection, contract_controller):
		self._db_connection = db_connection
		self._contract_controller = contract_controller

		self._project_dict = dict()

	def add_project(self, name, contract):
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Projects (Name, ContractId) VALUES (?, ?)"
		db_cursor.execute(query, [name, contract.contract_id])
		project_id = db_cursor.lastrowid

		self._db_connection.commit()

		project = Project(project_id, name, contract)

		return project

	def get_all_projects_dict(self):
		contract_dict = self._contract_controller.get_all_contracts_dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Projects"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			project_id = row[0]

			if project_id in self._project_dict:
				project = self._update_project_from_row(row, contract_dict, self._project_dict[project_id])
			else:
				project = self._create_project_from_row(row, contract_dict)

			self._projects_dict[project.project_id] = project

		return self._projects_dict

	def _create_project_from_row(self, row, contract_dict):
		project_id = row[0]
		name = row[1]
		contract_id = row[2]

		project = Project(project_id, name, contract_dict[contract_id])
		return project
		
	def _update_project_from_row(self, row, contract_dict, project):
		project.name = row[1]
		project.contract = contract_dict[row[2]]

		return project
