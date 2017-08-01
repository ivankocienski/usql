from query import Count
import unittest

class TestCount(unittest.TestCase):
    def test_count(self):

        q = Count().q_table("users") 
        sql, args = q.to_sql()

        ex_sql = "SELECT COUNT(*) FROM users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_where(self):

        q = Count().q_table("users").q_where("age>?", 123)
        sql, args = q.to_sql()

        ex_sql = "SELECT COUNT(*) FROM users WHERE (age>?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [123])

if __name__ == '__main__':
    unittest.main()

