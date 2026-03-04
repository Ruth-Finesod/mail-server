from typing import Dict, List

DB = "mail_server_db.db"

SELECT = f"""
SELECT *
FROM table """

INSERT = f"""
INSERT INTO table VALUES"""

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
        query = SELECT.replece('table', table_name)
        query += f"WHERE {q.items()[0][0]}={q.items()[0][1]}"
        if len(q.items()) > 1:
            for key, item in q.items()[1:]:
                query += f"AND {key}={item}"
        self.cur.execute(query)
        return self.cur.fetchall()


    def write(self, table_name, row: Dict):
        self.varify_keys(table_name, q.keys())
        self.cur.execute(INSERT.replece('table', table_name), row.items())

class NoSuchColumnError(Exception):
    pass


