
from query import Delete
import unittest

class TestSelect(unittest.TestCase):
    def test_delete(self):

        q = Delete().q_from("users") 
        sql, args = q.to_sql()

        ex_sql = "DELETE FROM users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)


if __name__ == '__main__':
    unittest.main()

