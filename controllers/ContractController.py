import dateutil.parser

from domain import *

class ContractController:
	def __init__(self, db_connection):
		# TODO: Comment
		self._db_connection = db_connection
		self._contracts_dict = dict()

	def create_contract(self, name, start, end, hours):
		# TODO: Comment
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
		db_cursor.execute(query, [name, self._python_datetime_to_sql(start), self._python_datetime_to_sql(end), hours])
		contract_id = db_cursor.lastrowid

		self._db_connection.commit()

		contract = Contract(contract_id, name, str(start), str(end), hours)

		return contract

	def retrieve_all_contracts(self):
		"""Returns a dictionary containing all contracts in the database
		
		The returned dictionary maps contract_ids to their respective contract"""

		# Initialize return_value
		return_value = {}

		# Actually query database
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Contracts"
		db_cursor.execute(query)

		# Create objects from returned rows
		for row in db_cursor.fetchall():
			contract = self._create_contract_from_row(row)
			return_value[contract.contract_id] = contract

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
		start = self._sql_datetime_to_python(row[2])
		end = self._sql_datetime_to_python(row[3])
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
