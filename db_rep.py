import sqlite3


class Database:
    def __init__(self, fname: str):
        self.file = fname

        self.conn = sqlite3.connect(self.file, check_same_thread=False)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_table(self, table: str, name: str):
        data = f'''CREATE TABLE {table}({name})'''
        self.cur.execute(data)
        self.conn.commit()

    def insert_table(self, table: str, data: str, indata: str):
        p = f"INSERT INTO {table}({data}) VALUES(?)"
        self.cur.execute(p, [indata])
        self.conn.commit()

    def insert_table_args(self, table: str, data: str, *args):
        aa = ''
        for _ in range(len(args)):
            aa += '?,'
        aa = aa[:-1]
        p = f'INSERT INTO {table}({data}) VALUES({aa})'
        self.cur.execute(p, args)
        self.conn.commit()

    def select_table(self, data: str, table: str):
        select = f"SELECT {table} FROM {data}"
        self.cur.execute(select)
        rows = self.cur.fetchall()
        result = []
        for row in rows:
            if len(row) == 1:
                result.append(row[0])
            else:
                result.append(row)
        return result

    def delete_data(self, table: str, data: str, delete: str):
        dels = f"DELETE FROM {table} WHERE {data} = ?"
        self.cur.execute(dels, [delete])
        self.conn.commit()

    def delete_teble(self, table: str):
        delete = f"DROP TABLE {table}"
        self.cur.execute(delete)
