import sqlite3
import unittest

from query import Count, Select, Delete, Update, Insert

DB_NAME = 'test-database.sqlite3'

_db = None

#
# DB support
#

def init_db():
    global _db 
    print("using DB %s" % DB_NAME)
    _db = sqlite3.connect(DB_NAME)
    #_db.set_trace_callback(print)

def make_schema():
    print("making schema")

    sql  = "CREATE TABLE IF NOT EXISTS users ("
    sql += "  id integer primary key,"
    sql += "  name varchar(30),"
    sql += "  sport varchar(30),"
    sql += "  age integer"
    sql += "  )"

    _db.execute(sql)


def clear_db():
    #print("clearing tables")

    sql = "DELETE FROM users"
    _db.execute(sql)

class StatementResult:
    # this seems redundant -.-

    def __init__(self, op):
        self._op = op

        sql, args = op.to_sql()
        self._cursor = _db.cursor()
        self._cursor.execute(sql, args)

    def first_record(self):
        return self._cursor.fetchone()

    def all_records(self):
        return self._cursor.fetchall()

    def last_id(self):
        return self._cursor.lastrowid

    def row_count(self):
        return self._cursor.rowcount


#
# test classes
#

class _TestCommon(unittest.TestCase):

    def tearDown(self):
        clear_db()

class TestInsert(_TestCommon):

    def test_insert(self):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)
        self.assertIsInstance(res.last_id(), int)


class TestUpdate(_TestCommon):

    def test_update(self):
        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)

        op = Update().\
                q_table("users").\
                q_set("name", "max").\
                q_set("age", 20)

        res = StatementResult(op)
        
        self.assertEqual(res.row_count(), 1)

class TestDelete(_TestCommon):

    def test_delete(self):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)

        op = Delete().\
                q_from("users")

        res = StatementResult(op)
        
        self.assertEqual(res.row_count(), 1)


class TestSelect(_TestCommon):

    def test_select(self):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)

        op = Select().\
                q_from("users")

        res = StatementResult(op)
        rows = res.all_records()
        
        self.assertEqual(len(rows), 1)

#
# main
#

if __name__ == '__main__':
    init_db()
    make_schema()
    clear_db()

    unittest.main()

