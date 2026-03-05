from typing import Dict, List
import sqlite3

DB = "mail_server_db.db"

SELECT = """
SELECT *
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


class DBHandler:
    def __init__(self):
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()

    @staticmethod
    def varify_keys(table_name, keys: List[str]):
        if table_name == 'users':
            columns = USERS_COLUMNS
        if table_name == 'msgs':
            columns = MSGS_COLUMNS
        for key in keys:
            if key not in columns:
                raise NoSuchColumnError

    def query(self, table_name, q: Dict) -> List[Dict]:
        self.varify_keys(table_name, q.keys())
        query = SELECT.replace('table', table_name)
        item = q.popitem()
        if type(item[1]) == str:
            query += f"WHERE {item[0]}='{item[1]}'"
        else:
            query += f"WHERE {item[0]}={item[1]}"
        for key, item in q.items():
            if type(item[1]) == str:
                query += f"AND {key}='{item}'"
            else:
                query += f"AND {key}={item}"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_uid(self, table_name):
        self.cur.execute(MAX.replace('table', table_name))
        max_uid = self.cur.fetchone()
        if max_uid[0]:
            return max_uid[0] + 1
        else:
            return 1

    def write(self, table_name, row: Dict):
        self.varify_keys(table_name, row.keys())
        row['uid'] = self.get_uid(table_name)
        print(row)
        self.cur.execute(
            f"{INSERT.replace('table', table_name)} {str(tuple(row.keys()))} VALUES{str(tuple(row.values()))}")
        self.con.commit()

    def close(self):
        self.con.close()


class NoSuchColumnError(Exception):
    pass
