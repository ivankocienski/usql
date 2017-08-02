import sqlite3
import unittest

from usql.statement import Count, Select, Delete, Update, Insert

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

    def integer(self):
        return self.first_record()[0]



#
# test classes
#

class _TestCommon(unittest.TestCase):

    def tearDown(self):
        clear_db()

class _InsertCommon():

    def _insert_user(self, name, sport, age):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values(name, sport, age)

        res = StatementResult(op)
        return res.last_id()
    
    def _insert_common_users(self):
        r = []
        r.append(self._insert_user("user-1", "alpha", 100))
        r.append(self._insert_user("user-2", "beta",  101))
        r.append(self._insert_user("user-3", "cappa", 102))
        r.append(self._insert_user("user-4", "delta", 103))
        return r

class TestInsert(_TestCommon, _InsertCommon):

    def test_insert(self):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)
        self.assertIsInstance(res.last_id(), int)

    def test_insert_multiple(self):

        self._insert_common_users()

        op = Count().q_table("users")
        res = StatementResult(op)

        self.assertEqual(res.integer(), 4)


class TestCount(_TestCommon, _InsertCommon):

    def test_count(self):

        op = Insert().\
                q_table("users").\
                q_columns("name", "sport", "age").\
                q_values("jerry", "alpha", 123)

        res = StatementResult(op)

        op = Count().q_table("users")
        res = StatementResult(op)

        self.assertEqual(res.integer(), 1)

    def test_count_where(self):

        self._insert_common_users()

        op = Count().\
                q_table("users").\
                q_where("age>?", 101)

        res = StatementResult(op) 
        self.assertEqual(res.integer(), 2)

class TestUpdate(_TestCommon, _InsertCommon):

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

    def test_update_single(self):

        r = self._insert_common_users()

        op = Update().\
                q_table("users").\
                q_set("name", "max").\
                q_set("age", 20).\
                q_where("id=?", r[0])

        res = StatementResult(op) 
        self.assertEqual(res.row_count(), 1)

    def test_update_multiple(self):

        r = self._insert_common_users()

        op = Update().\
                q_table("users").\
                q_set("sport", "zappa").\
                q_where("age>?", 101)

        res = StatementResult(op) 
        self.assertEqual(res.row_count(), 2)


class TestDelete(_TestCommon, _InsertCommon):

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

    def test_delete_multiple(self):

        r = self._insert_common_users()

        op = Delete().q_from("users") 
        res = StatementResult(op)

        self.assertEqual(res.row_count(), 4)

    def test_delete_single(self):

        r = self._insert_common_users()

        op = Delete().q_from("users").q_where("id=?", r[0])
        res = StatementResult(op)

        self.assertEqual(res.row_count(), 1)

        op = Count().q_table("users")
        res = StatementResult(op)

        self.assertEqual(res.integer(), 3)

    def test_delete_multiple(self):

        self._insert_common_users()

        op = Delete().q_from("users").q_where("age>?", 101)
        res = StatementResult(op)

        self.assertEqual(res.row_count(), 2)

        op = Count().q_table("users")
        res = StatementResult(op)

        self.assertEqual(res.integer(), 2)


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

def integrated_setup():
    init_db()
    make_schema()
    clear_db()

if __name__ == '__main__':
    integrated_setup()

    unittest.main()

