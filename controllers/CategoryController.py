from domain import *

class CategoryController:
	def __init__(self, db_connection):
		self._db_connection = db_connection
		self._categories_dict = dict()

	def add_category(self, name):
		db_cursor = self._db_connection.cursor()

		query = "INSERT INTO Categories (Name) VALUES (?)"
		db_cursor.execute(query, [name])
		category_id = db_cursor.lastrowid

		self._db_connection.commit()

		category = Category(category_id, name)

	def get_all_categories_dict(self):
		db_cursor = self._db_connection.cursor()
		query = "SELECT * FROM Categories"
		db_cursor.execute(query)

		for row in db_cursor.fetchall():
			category_id = row[0]

			if category_id in self._categories_dict:
				category = self._update_category_from_row(row, self._categories_dict[category_id])
			else:
				category = self._create_category_from_row(row)

			self._categories_dict[category.category_id] = category

		return self._categories_dict

	def _create_category_from_row(self, row):
		category_id = row[0]
		name = row[1]

		category = Category(category_id, name)
		return category

	def _update_category_from_row(self, row, category):
		category.name = row[1]

		return category
