import pymysql
from pymysql import connect

from .BaseDataService import DataDataService
from datetime import datetime


class MySQLRDBDataService(DataDataService):
    """
    A generic data service for MySQL databases. The class implement common
    methods from BaseDataService and other methods for MySQL. More complex use cases
    can subclass, reuse methods and extend.
    """

    def __init__(self, context):
        super().__init__(context)

    def _get_connection(self):
        connection = pymysql.connect(
            host=self.context["host"],
            port=self.context["port"],
            user=self.context["user"],
            passwd=self.context["password"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return connection

    def get_data_object(self,
                        database_name: str,
                        collection_name: str,
                        key_field: str,
                        key_value: str,
                        fetch_all: bool = False,):
        """
        See base class for comments.
        """

        connection = None
        result = None

        try:
            sql_statement = f"SELECT * FROM {database_name}.{collection_name} " + \
                        f"where {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            # Fetch results
            if fetch_all:
                result = cursor.fetchall()  # Fetch all matching records
            else:
                result = cursor.fetchone()  # Fetch a single record
        except Exception as e:
            if connection:
                connection.close()

        return result

    def delete_data_object(self,
                           database_name: str,
                           collection_name: str,
                           key_field: str,
                           key_value: str):
        connection = None
        success = False

        try:
            # Construct the SQL DELETE statement
            sql_statement = f"DELETE FROM {database_name}.{collection_name} WHERE {key_field}=%s"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, [key_value])
            # Check if any rows were affected
            if cursor.rowcount > 0:
                success = True
        except Exception as e:
            print(f"Error deleting data object: {e}")
        finally:
            if connection:
                connection.close()
        return success

    def add_data_object(self,
                        database_name: str,
                        collection_name: str,
                        data: dict):
        connection = None
        success = False

        try:
            current_time = datetime.now()
            if collection_name == "info_collection" and "created_at" not in data:
                data["created_at"] = current_time
            if collection_name == "content_collection" and "added_at" not in data:
                data["added_at"] = current_time

            sql_statement = f"INSERT INTO {database_name}.{collection_name} " + \
                f"({', '.join(data.keys())}) " + \
                f"VALUES ({', '.join(['%s'] * len(data))})"
            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(data.values()))
            success = True
        except Exception as e:
            if connection:
                connection.close()
        return success

    def update_data_object(self,
                           database_name: str,
                           collection_name: str,
                           key_field: str,
                           key_value: str,
                           data: dict):
        connection = None
        success = False

        try:
            current_time = datetime.now()
            if collection_name == "info_collection" and "created_at" not in data:
                data["created_at"] = current_time
            if collection_name == "content_collection" and "added_at" not in data:
                data["added_at"] = current_time

            set_clause = ", ".join([f"{key}=%s" for key in data.keys()])
            sql_statement = f"UPDATE {database_name}.{collection_name} SET {set_clause} WHERE {key_field}=%s"

            connection = self._get_connection()
            cursor = connection.cursor()
            cursor.execute(sql_statement, list(data.values()) + [key_value])
            connection.commit()

            result = cursor.rowcount
            print(f"Updated {result} row(s).")
            if cursor.rowcount > 0:
                success = True
        except Exception as e:
            print(f"Error updating data object: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

        return success










