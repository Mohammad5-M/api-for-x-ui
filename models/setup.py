import sqlite3
import json


class SqliteDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()
        self.conn.row_factory = sqlite3.Row

    def add_row(self, table_name, values):
        placeholders = ", ".join("?" * len(values))
        query = f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def port_exist(self, port):
        query = f"SELECT port FROM inbounds WHERE port = ?"
        self.cursor.execute(query, (port,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def all_exist_with_port(self, port):
        query = f"SELECT * FROM inbounds WHERE port = ?"
        self.cursor.execute(query, (port,))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def all_user_traffic_with_email(self, email):
        query = f"SELECT * FROM client_traffics WHERE email = ?"
        self.cursor.execute(query, (email,))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def all_admin_traffic_with_uuid(self, port, uuid):
        query = f"SELECT * FROM client_traffics WHERE email = ?"
        # print(self.get_settings(port))
        sett = json.loads(self.get_settings(port))
        res = list(
            filter(lambda test_list: test_list['id'] == uuid, sett["clients"]))
        print(res)
        self.cursor.execute(query, (res[0]["email"],))
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            return None

    def get_settings(self, port):
        query = f"SELECT settings FROM inbounds WHERE port = ?"
        self.cursor.execute(query, (port,))
        row = self.cursor.fetchone()
        if row:
            return row[0]
        else:
            return None

    def client_settings_updator(self, port, settings: dict):
        # update the settings for the given id
        sett = json.loads(self.get_settings(port))
        sett["clients"].append(settings)
        # print(sett)
        self.conn.execute(
            "UPDATE inbounds SET settings = ? WHERE port = ?", (json.dumps(sett, indent=2), port))
        # commit the changes and close the connection
        self.conn.commit()
        # print(settings["totalGB"])

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.close()
