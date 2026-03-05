import sqlite3
from typing import Dict, List, Any, Tuple

DB = "mail_server_db.db"

SELECT = """SELECT *
FROM table
"""

INSERT = """
INSERT INTO table 
"""

UPDATE = """
UPDATE table
"""

MAX = """
SELECT MAX(uid)
FROM table
"""

MSGS_COLUMNS = ['sender_uid', 'receiver_uid', 'subject', 'message', 'send_time', 'read', 'conv_uid']
USERS_COLUMNS = ['uid', 'email', 'name', 'password']


class NoSuchColumnError(Exception):
    pass


class NoSuchTableError(Exception):
    pass


class DBHandler:
    def __init__(self):
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()

    @staticmethod
    def verify_keys(table_name: str, keys: List[str]):
        if table_name == 'users':
            columns = USERS_COLUMNS
        elif table_name == 'msgs':
            columns = MSGS_COLUMNS
        else:
            raise NoSuchTableError('the requested table does not exist')
        for key in keys:
            if key not in columns:
                raise NoSuchColumnError("the columns in the filter does not match the table")

    def query(self, table_name: str, filters: Dict[str, Any]) -> List[Tuple]:
        """
        preforms a query based on a table name and filters in a dict
        :param table_name: the name of the table in the db
        :param filters: dict with the keys as columns names and values as their values
        :return: list of
        """
        self.verify_keys(table_name, list(filters.keys()))
        query = SELECT.replace('table', table_name)
        if filters:
            item = filters.popitem()
            query += f"WHERE {item[0]}={repr(item[1])}"
        for key, value in filters.items():
            query += f"AND {key}={repr(value)}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_uid(self, table_name: str):
        """gets the next uid in table table_name"""
        self.cur.execute(MAX.replace('table', table_name))
        max_uid = self.cur.fetchone()
        if max_uid[0]:
            return max_uid[0] + 1
        else:
            return 1

    def write(self, table_name: str, row: Dict[str, Any]):
        """writes a new row to table_name. the row given in the format of {column: value}"""
        self.verify_keys(table_name, list(row.keys()))
        row['uid'] = self.get_uid(table_name)
        print(row)
        self.cur.execute(
            f"{INSERT.replace('table', table_name)} {str(tuple(row.keys()))} VALUES{str(tuple(row.values()))}")
        self.con.commit()

    def update(self, table_name: str, filters: Dict[str, Any],  change: Dict[str, Any]):
        """writes a new row to table_name. the row given in the format of {column: value}"""
        self.verify_keys(table_name, list(filters.keys()))
        self.verify_keys(table_name, list(change.keys()))
        query = UPDATE.replace('table', table_name)
        if change:
            item = change.popitem()
            query += f"SET {item[0]}={repr(item[1])}"
        else:
            return
        for key, value in change.items():
            query += f", {key}={repr(value)}"
        if filters:
            item = filters.popitem()
            query += f"\nWHERE {item[0]}={repr(item[1])}"
        for key, value in filters.items():
            query += f"AND {key}={repr(value)}"
        self.cur.execute(query)
        self.con.commit()
