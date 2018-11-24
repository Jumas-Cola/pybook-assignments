import sqlite3


class DataBase:
    def __init__(self, db='db'):
        self.conn = sqlite3.connect(f"{db}.sqlite3")
        self.cursor = self.conn.cursor()

    def get_columns(self, tbl_name):
        self.sql_rows = f"SELECT * FROM {tbl_name}"
        columns = f"PRAGMA table_info({tbl_name})"
        self.cursor.execute(columns)
        return [row[1] for row in self.cursor.fetchall()]

    def limit(self, tbl_name, N=1):
        columns = self.get_columns(tbl_name)
        return Query(self.cursor, self.sql_rows + f" LIMIT {N}", columns, tbl_name)

    def insert(self, tbl_name, obj):
        cursor = self.cursor
        cursor.executemany(f'INSERT INTO {tbl_name} VALUES (?,?,?,?)', [obj])
        self.conn.commit()

    def Table(self, tbl_name):
        columns = self.get_columns(tbl_name)
        return Query(self.cursor, self.sql_rows, columns, tbl_name)


class Query:
    def __init__(self, cursor, rows, columns, tbl_name):
        self.cursor = cursor
        self.sql_rows = rows
        self.columns = columns
        self.tbl_name = tbl_name

    def filter(self, criteria):
        key_word = "AND" if "WHERE" in self.sql_rows else "WHERE"
        sql = f"{self.sql_rows} {key_word} {criteria}"
        return Query(self.cursor, sql, self.columns, self.tbl_name)

    def order_by(self, criteria):
        return Query(self.cursor, f"{self.sql_rows} ORDER BY {criteria}", self.columns, self.tbl_name)

    def group_by(self, criteria):
        return Query(self.cursor, f"{self.sql_rows} GROUP BY {criteria}", self.columns, self.tbl_name)

    @property
    def rows(self):
        print(self.sql_rows)
        self.cursor.execute(self.sql_rows)
        return [Row(zip(self.columns, fields), self.tbl_name) for fields in self.cursor.fetchall()]


class Row:
    def __init__(self, fields, table_name):
        self.__class__.__name__ = "User"

        for name, value in fields:
            setattr(self, name, value)

    def __repr__(self):
        attrs =  ', '.join([f"{attr}={value}" for attr, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attrs})"


db = DataBase('users_db')
print(db.get_columns('users'))
print(db.limit('users',2).rows)
db.insert('users', (5, 'john', 'john@thebeatles.com', 'foobar'))
