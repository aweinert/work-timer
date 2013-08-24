import sqlite3

class Database:
    def __init__(self, path):
        self._db_connection = sqlite3.connect(path)
        
    def retrieve_single_row(self, query, arguments = None):
        """Executes the query and retrieves the single line returned by it
        
        If not exactly one line is retrieved, None is returned.
        TODO: Raise exception in case of none or multiple lines"""
        cursor = self._db_connection.cursor()
        
        self._execute_query(cursor, query, arguments)
            
        results = cursor.fetchall()
        
        if len(results) <> 1:
            return None
        else:
            return results[0]
            
    def retrieve_rows(self, query, arguments = None):
        """Executes the given query and returns its results.
        
        The resulting list may be empty or contain multiple rows"""
        cursor = self._db_connection.cursor()
        
        self._execute_query(cursor, query, arguments)
            
        return cursor.fetchall()

    def create_single_row(self, query, arguments = None):
        """Executes the given query and returns the last inserted row_id"""
        cursor = self._db_connection.cursor()
        
        self._execute_query(cursor, query, arguments)
        last_row_id = cursor.lastrowid
        self._db_connection.commit()
        
        return last_row_id
    
    def update_rows(self, query, arguments = None):
        """Executes the given query and commits the results
        
        Until now the difference between this and delete_rows
        is purely syntactical.
        TODO: Handle errors differently in both functions"""
        cursor = self._db_connection.cursor()
        self._execute_query(cursor, query, arguments)
        self._db_connection.commit()

    def delete_rows(self, query, arguments = None):
        """Executes the given query and commits the results
        
        Until now the difference between this and update_rows
        is purely syntactical.
        TODO: Handle errors differently in both functions"""
        cursor = self._db_connection.cursor()
        self._execute_query(cursor, query, arguments)
        self._db_connection.commit()

            
    def _execute_query(self, cursor, query, arguments):
        if arguments <> None:
            cursor.execute(query, arguments)
        else:
            cursor.execute(query)