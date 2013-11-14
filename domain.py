import datetime

class Contract:
	def __init__(self, contract_id, name, start, end, hours):
		self.contract_id = contract_id
		self.name = name
		self.start = start
		self.end = end
		self.hours = hours
		
	def __str__(self):
		return self.name + ", " + str(self.hours) + "h (" + str(self.start) + " - " + str(self.end) + ")"
	
	def __eq__(self, other):
		if not isinstance(other, Contract):
			return NotImplemented
		if not self.contract_id == other.contract_id:
			return False
		if not self.name == other.name:
			return False
		if not self.start == other.start:
			return False
		if not self.end == other.end:
			return False
		if not self.hours == other.hours:
			return False

class Project:
	def __init__(self, project_id, name, contract):
		self.project_id = project_id
		self.name = name
		self.contract = contract
		
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		if not isinstance(other, Project):
			return NotImplemented
		if not self.project_id == other.project_id:
			return False
		if not self.name == other.name:
			return False
		if not self.contract == other.contract:
			return False

class Category:
	def __init__(self, category_id, name):
		self.category_id = category_id
		self.name = name
		
	def __str__(self):
		return self.name
	
	def __eq__(self, other):
		if not isinstance(other, Category):
			return NotImplemented
		if not self.category_id == other.category_id:
			return False
		if not self.name == other.name:
			return False

class Worktime:
	def __init__(self, time_id, project, category, start, end, description):
		self.time_id = time_id
		self.project = project
		self.category = category
		self.start = start
		self.end = end
		self.description = description

	def get_duration(self):
		if self.end == None:
			return datetime.datetime.now() - self.start
		else:
			return self.end - self.start
	
	def __str__(self):
		if self.start.date() == self.end.date():
			return self.start.date() + " " + self.start.time() + " - " + self.end.time() + ": " + self.description
		else:
			return self.start.date() + " " + self.start.time() + " - " + self.end.date() + " " + self.end.time() + ": " + self.description

	def __eq__(self, other):
		if not isinstance(other, Worktime):
			return NotImplemented
		if not self.time_id == other.time_id:
			return False
		if not self.project == other.project:
			return False
		if not self.category == other.category:
			return False
		if not self.start == other.start:
			return False
		if not self.end == other.end:
			return False
		if not self.description == other.description:
			return False