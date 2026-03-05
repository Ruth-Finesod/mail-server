import sqlite3
from typing import Dict, List, Any, Tuple

DB = "mail_server_db.db"

SELECT = """SELECT *
FROM table
"""

INSERT = """
INSERT INTO table 
"""

MAX = """
SELECT MAX(uid)
FROM table
"""

MSGS_COLUMNS = ['sender_uid', 'receiver_uid', 'subject', 'message', 'send_time']
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
    def verify_keys(table_name, keys: List[str]):
        if table_name == 'users':
            columns = USERS_COLUMNS
        elif table_name == 'msgs':
            columns = MSGS_COLUMNS
        else:
            raise NoSuchTableError('the requested table does not exist')
        for key in keys:
            if key not in columns:
                raise NoSuchColumnError("the columns in the filter does not match the table")

    def query(self, table_name, filters: Dict[str, Any]) -> List[Tuple]:
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
            value = "'" + item[1] + "'" if type(item[1]) is str else item[1]
            query += f"WHERE {item[0]}={value}"
        for key, value in filters.items():
            value = "'" + value + "'" if type(value) is str else value
            query += f"AND {key}={value}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_uid(self, table_name):
        """gets the next uid in table table_name"""
        self.cur.execute(MAX.replace('table', table_name))
        max_uid = self.cur.fetchone()
        if max_uid[0]:
            return max_uid[0] + 1
        else:
            return 1

    def write(self, table_name, row: Dict[str, Any]):
        """writes a new row to table_name. the row given in the format of {column: value}"""
        self.verify_keys(table_name, list(row.keys()))
        row['uid'] = self.get_uid(table_name)
        print(row)
        self.cur.execute(
            f"{INSERT.replace('table', table_name)} {str(tuple(row.keys()))} VALUES{str(tuple(row.values()))}")
        self.con.commit()

    def close(self):
        """closes the connection to the db"""
        self.con.close()
