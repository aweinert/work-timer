import dateutil.parser

from domain import *

class WorktimeController:
	def __init__(self, db_connection, project_controller, contract_controller):
		self._db_connection = db_connection
		self._project_controller = project_controller
		self._contract_controller = contract_controller

		self._worktime_dict = dict()

	def add_worktime(self, project, category, start, end, description):
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Times (ProjectId, CategoryId, Start, End, Description) VALUES (?,?,?,?,?)"
		db_cursor.execute(query, [project.project_id, category.category_id, str(start), str(end), description])
		worktime_id = db_cursor.lastrowid

		self._db_connection.commit()

		worktime = Worktime(worktime_id, project.project_id, category.category_id, start, end, description)

		return worktime

	def get_all_worktimes_dict(self):
		project_dict = self._project_controller.get_all_projects_dict()
		category_dict = self._category_controller.get_all_categories_dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Times"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			worktime_id = row[0]

			if worktime_id in self._worktime_dict:
				worktime = self._update_worktime_from_row(row, project_dict, category_dict, self._worktime_dict[worktime_id])
			else:
				worktime = self._create_worktime_from_row(row, project_dict, category_dict)

			self._worktime_dict[time_id] = worktime

		return self._worktime_dict

	def _create_worktime_from_row(self, row, project_dict, category_dict):
		time_id = row[0]
		project_id = row[1]
		category_id = row[2]
		start = dateutil.parser.parse(row[3])
		end = dateutil.parser.parse(row[4])
		description = row[5]

		worktime = Worktime(time_id, project_dict[project_id], category_dict[category_id], start, end, description)
		return worktime

	def _update_worktime_from_row(self, row, project_dict, category_dict, worktime):
		worktime.project = project_dict[row[1]]
		worktime.category = category_dict[row[2]]
		worktime.start = dateutil.parser.parse(row[3])
		worktime.end = dateutil.parser.parse(row[4])
		worktime.description = row[5]

		return worktime
