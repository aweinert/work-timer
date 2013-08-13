from domain import *

class CategoryController:
	def __init__(self, db_connection):
		# TODO: Comment
		self._db_connection = db_connection
		self._categories_dict = dict()

	def create_category(self, name):
		# TODO: Comment
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Categories (Name) VALUES (?)"
		db_cursor.execute(query, [name])
		category_id = db_cursor.lastrowid

		self._db_connection.commit()

		category = Category(category_id, name)
		return category

	def retrieve_all_categories(self):
		"""Returns a dictionary containing all categories in the database
		
		The returned dictionary maps category_ids to their respective category"""
		return_value = {}
		
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Categories"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			category = self._create_category_from_row(row)
			return_value[category.category_id] = category

		return return_value
	
	def retrieve_category_by_id(self, category_id):
		"""Returns the category with the given id, if it exists in the database.
		
		If there is no category with the given id, None is returned"""
		db_cursor = self._db_connection.cursor()

		query = "SELECT * FROM Categories WHERE CategoryId = ?"
		db_cursor.execute(query, category_id)

		results = db_cursor.fetchall()
		if len(results) <> 1:
			return_value = None
		else:
			return_value = self._create_contract_from_row(results[0])
			
		return return_value
		
	def update_category(self, category):
		"""Writes the changes made in the given contract to the database"""
		db_cursor = self._db_connection.cursor()
		
		query = "UPDATE Categories SET (name = ?) WHERE CategoryId = ?"
		db_cursor.execute(query, category.name, category.category_id)
		
		self._db_connection.commit()
		
	def delete_category(self, category):
		"""Removes the given category from the database.
		
		The given category is considered invalid after a call to this method"""
		db_cursor = self._db_connection.cursor()
		
		query = "DELETE FROM Categories WHERE CategoryId = ?"
		db_cursor.execute(query, category.category_id)
		
		self._db_connection.commit()

	def _create_category_from_row(self, row):
		# TODO: Comment
		category_id = row[0]
		name = row[1]

		category = Category(category_id, name)
		return category

	def _update_category_from_row(self, row, category):
		# TODO: Comment
		category.name = row[1]

		return category
