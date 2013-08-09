import dateutil.parser

from domain import *

class ContractController:
	def __init__(self, db_connection):
		self._db_connection = db_connection
		self._contracts_dict = dict()

	def add_contract(self, name, start, end, hours):
		db_cursor = self._db_connection.cursor()

		if start <> None:
			start_param = str(start)
		else:
			start_param = None

		if end <> None:
			end_param = str(end)
		else:
			end_param = None

		query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
		db_cursor.execute(query, [name, start_param, end_param, hours])
		contract_id = db_cursor.lastrowid

		self._db_connection.commit()

		contract = Contract(contract_id, name, str(start), str(end), hours)

		return contract

	def get_all_contracts_dict(self):
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Contracts"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			contract_id = row[0]

			if contract_id in self._contracts_dict:
				contract = self._update_contract_from_row(row, self._contracts_dict[contract_id])
			else:
				contract = self._create_contract_from_row(row)
				
			self._contracts_dict[contract.contract_id] = contract

		return self._contracts_dict

	def _create_contract_from_row(self, row):
		contract_id = row[0]
		name = row[1]

		if row[2] <> None:
			start = dateutil.parser.parse(row[2]).date()
		else:
			start = None

		if row[3] <> None:
			end = dateutil.parser.parse(row[3]).date()
		else:
			end = None

		hours = row[4]

		contract = Contract(contract_id, name, start, end, hours)
		return contract

	def _update_contract_from_row(self, row, contract):
		contract.name = row[1]
		contract.start = dateutil.parser.parse(row[2]).date()
		contract.end = dateutil.parser.parse(row[3]).date()
		contract.hours = row[4]
	
		return contract
		
