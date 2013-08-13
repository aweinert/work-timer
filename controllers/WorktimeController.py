import dateutil.parser
import datetime

from domain import *

class WorktimeController:
	def __init__(self, db_connection, project_controller, contract_controller):
		self._db_connection = db_connection
		self._project_controller = project_controller
		self._contract_controller = contract_controller

		self._worktime_dict = dict()

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

		project_dict = self._project_controller.get_all_projects_dict()
		category_dict = self._category_controller.get_all_categories_dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Times"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			worktime = self._create_worktime_from_row(row, project_dict, category_dict)
			return_value.append(worktime)

		return return_value

	def retrieve_worktime_by_id(self, worktime_id):
		"""Returns the worktime with the given id, if it exists in the database.
		
		If there is no worktime with the given id, None is returned"""
		project_dict = self._project_controller.get_all_projects_dict()
		category_dict = self._category_controller.get_all_categories_dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Times WHERE TimeId = ?"
		db_cursor.execute(query, worktime_id)

		results = db_cursor.fetchall()
		
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_worktime_from_row(results[0], project_dict, category_dict)

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
		

	def _create_worktime_from_row(self, row, project_dict, category_dict):
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

		worktime = Worktime(time_id, project_dict[project_id], category_dict[category_id], start, end, description)
		return worktime