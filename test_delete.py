
from query import Delete
import unittest

class TestSelect(unittest.TestCase):
    def test_delete(self):

        q = Delete().q_from("users") 
        sql, args = q.to_sql()

        ex_sql = "DELETE FROM users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_where(self):

        q = Delete().q_from("users").q_where("id=?", 123)
        sql, args = q.to_sql()

        ex_sql = "DELETE FROM users WHERE (id=?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [123])

if __name__ == '__main__':
    unittest.main()

