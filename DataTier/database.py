import sqlite3


# We create a database object
class DataBase:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table_if_not_exists(self, table_name, columns):
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                            f'{columns})')
        self.connection.commit()

    def try_to_add_to_table(self, table_name, columns, values):
        self.cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({values})')
        self.connection.commit()

    def update_stock_from_table(self, table_name, column, value, ide):
        stock = self.cursor.execute(f'SELECT {column} FROM {table_name} WHERE ID = {ide}').fetchone()[0]
        self.cursor.execute(f'UPDATE {table_name} SET {column} = {stock-value} WHERE ID = {ide}')
        self.connection.commit()

    def update_table_for_strings(self, table_name, column, value, ide):
        self.cursor.execute(f'UPDATE {table_name} SET {column} = "{value}" WHERE ID = {ide}')
        self.connection.commit()

    def update_table_for_any_other(self, table_name, column, value, ide):
        self.cursor.execute(f'UPDATE {table_name} SET {column} = {value} WHERE ID = {ide}')
        self.connection.commit()

    def query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def return_table_names(self):
        return self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    def list_columns_of_a_table(self, table_name):
        return self.cursor.execute(f'PRAGMA table_info({table_name})').fetchall()

    def change_table_name(self, old_name, new_name):
        self.cursor.execute(f'ALTER TABLE {old_name} RENAME TO {new_name}')
        self.connection.commit()

    def __del__(self):
        self.connection.close()
