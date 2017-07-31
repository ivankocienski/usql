from query import Update
import unittest

class TestUpdate(unittest.TestCase):
    def test_table(self):

        q = Update().q_table("users") 
        sql, args = q.to_sql()

        ex_sql = "UPDATE users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_set(self):
        q = Update().q_table("users").q_set("name=?", 'jerry')
        sql, args = q.to_sql()

        ex_sql = "UPDATE users SET name=?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['jerry'])

    def test_set_multi(self):
        q = Update().q_table("users").\
                q_set("name=?", 'jerry').\
                q_set("age=?", 123)

        sql, args = q.to_sql()

        ex_sql = "UPDATE users SET name=?, age=?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['jerry', 123])

    def test_where(self):

        q = Update().q_table("users").q_where("id=?", 123)
        sql, args = q.to_sql()

        ex_sql = "UPDATE users WHERE (id=?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [123])

if __name__ == '__main__':
    unittest.main()

