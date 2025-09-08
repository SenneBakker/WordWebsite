import sqlite3


class DbConnection:
    def __init__(self, db_name: str, table_name):
        """
        Connect to db object. Creates db object if it doesn't exist yet.

        :param db_name:
        """
        self.db_name = db_name
        self.table_name = table_name
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER PRIMARY KEY UNIQUE, translation STRING, STRING, score FLOAT)")

    def get_records(self):
        """
        Get all records from db object

        :return: list of tuples
        """
        query = f"""SELECT * FROM {self.table_name}"""
        result = self.cur.execute(query)
        return result.fetchall()

    def add_records(self, records: list):
        """
        Adds a list of records to the specified database

        :param records: Records must be a list of tuples
        :return: None
        """
        query = f"""INSERT INTO {self.table_name} VALUES(?, ?, ?, ?)"""
        try:
            self.cur.executemany(query, records)
        except sqlite3.IntegrityError:
            print(f"ERROR: one or more records already exist in the table. Make sure the word's ID is unique.")
            pass
        self.con.commit()

    def add_record(self, record):
        """
        Add a single record to the database

        :param record: a tuple object
        :return: None
        """
        query = f"""INSERT INTO {self.table_name} VALUES {record}"""
        try:
            self.cur.execute(query)
        except sqlite3.IntegrityError:
            print(f"ERROR: the record already exist in the table. Make sure the word's ID is unique.")
            pass
        self.con.commit()

    def delete_record(self, record):
        query = f"DELETE FROM {self.table_name} WHERE id = {record[0]}"
        try:
            self.cur.execute(query)
        except:
            print("ERROR: no matching record found.")
            pass
        self.con.commit()

rec1 = (1, 'irmão', 'broer', 0)
rec2 = (2, 'irmã', 'zus', 0)
records = [rec1, rec2]
db = DbConnection("tutorial.db", "translations")
db.add_records(records)
print(db.get_records())

db.delete_record(rec1)
print(db.get_records())
