
from query import Insert
import unittest

class TestInsert(unittest.TestCase):
    def test_table(self):

        q = Insert().q_table("users") 
        sql, args = q.to_sql()

        ex_sql = "INSERT INTO users () VALUES ()"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_column(self): 
        q = Insert().q_table("users").q_columns("name")
        sql, args = q.to_sql()

        ex_sql = "INSERT INTO users (name) VALUES (?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_multiple_column(self): 
        q = Insert().q_table("users").q_columns("name", "age", "sport")
        sql, args = q.to_sql()

        ex_sql = "INSERT INTO users (name, age, sport) VALUES (?, ?, ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_multiple_column_2(self): 
        q = Insert().q_table("users").\
                q_columns("name").\
                q_columns("age").\
                q_columns("sport")

        sql, args = q.to_sql()

        ex_sql = "INSERT INTO users (name, age, sport) VALUES (?, ?, ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_values(self):
        q = Insert().q_table("users").\
                q_columns("name", "age", "sport").\
                q_values("jerry", 123, "tennis")

        sql, args = q.to_sql()

        ex_sql = "INSERT INTO users (name, age, sport) VALUES (?, ?, ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ["jerry", 123, "tennis"])

if __name__ == '__main__':
    unittest.main()

