import dateutil.parser

from domain import *

class ContractController:
	def __init__(self, db_connection):
		self._db_connection = db_connection

	def add_contract(self, name, start, end, hours):
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Contracts(Name, Start, End, Hours) Values(?,?,?,?)"
		db_cursor.execute(query, [name, start, end, hours])
		contract_id = db_cursor.lastrowid

		self._db_connection.commit()

		contract = Contract(contract_id, name, str(start), str(end), hours)

		return contract

	def get_all_contracts_dict(self):
		return_value = dict()

		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Contracts"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			contract = self._create_contract_from_row(row)
			return_value[contract.contract_id] = contract

		return return_value

	def _create_contract_from_row(self, row):
		contract_id = row[0]
		name = row[1]
		start = dateutil.parser.parse(row[2]).date()
		end = dateutil.parser.parse(row[3]).date()
		hours = row[4]

		contract = Contract(contract_id, name, start, end, hours)
		return contract
