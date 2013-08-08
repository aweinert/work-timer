class Contract:
	def __init__(self, contract_id, name, start, end, hours):
		self.contract_id = contract_id
		self.name = name
		self.start = start
		self.end = end
		self.hours = hours

class Project:
	def __init__(self, project_id, name, contract):
		self.project_id = project_id
		self.name = name
		self.contract = contract

class Category:
	def __init__(self, category_id, name):
		self.category_id = category_id
		self.name = name

class Worktime:
	def __init__(self, time_id, project, category, start, end, description):
		self.time_id = time_id
		self.project = project
		self.category = category
		self.start = start
		self.end = end
		self.description = description

	def get_duration(self):
		return self.end - self.start
