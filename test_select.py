
from query import Select
import unittest

class TestSelect(unittest.TestCase):
    def test_basic(self):

        q = Select().q_from("users") 
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    def test_one(self):

        q = Select().one().q_from("users")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users LIMIT ?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [1])
        self.assertTrue(q.as_one_record)

    # from multiple
    def test_from_multiple_tables(self):

        q = Select().q_from("users, posts")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users, posts"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    # select
    def test_select_fields(self):

        q = Select().q_from("users").q_select('id', 'email', 'name')
        sql, args = q.to_sql()

        ex_sql = "SELECT id, email, name FROM users"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    # joining
    def test_joining(self):

        q = Select().q_from("users").q_join("posts", "users.id = posts.user_id")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users JOIN posts ON users.id = posts.user_id"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    #def test_multi_joining(self):
    #    # TODO 

    #    q = Select().q_from("users").\ 
    #            q_join("posts", "users.id = posts.user_id").\
    #            q_join("tags", "tags.id = posts.tag_id")

    #    sql, args = q.to_sql()

    #    ex_sql = "SELECT * FROM users JOIN posts ON users.id = posts.user_id JOIN tags ON tags.id = posts.tag_id"

    #    self.assertEqual(sql, ex_sql)
    #    self.assertEqual(len(args), 0)


    # limit
    def test_limit(self):

        q = Select().q_from("users").q_limit(10)
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users LIMIT ?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [10])

    # offset
    def test_offset(self):

        q = Select().q_from("users").q_offset(20)
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users OFFSET ?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, [20])

    # order
    def test_order(self):

        q = Select().q_from("users").q_order_by("name")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users ORDER BY name"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(len(args), 0)

    # where
    def test_where_single(self):

        q = Select().q_from("users").q_where("name = ?", "jerry")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users WHERE (name = ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['jerry'])

    def test_where_multi(self):
        q = Select().q_from("users").\
                q_where("name = ?", "jerry").\
                q_where("age = ?", 123)

        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users WHERE (name = ?) AND (age = ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['jerry', 123])

    def test_where_or(self):

        q = Select().q_from("users").q_where("name = ? or age = ?", "jerry", 123)
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users WHERE (name = ? or age = ?)"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['jerry', 123])



    # (not-needed) distinct

    # group
    def test_group(self):

        q = Select().q_from("users").q_group_by("name")
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users GROUP BY ?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['name'])


    def test_group_having(self):

        q = Select().q_from("users").q_group_by("name", "id=?", 123)
        sql, args = q.to_sql()

        ex_sql = "SELECT * FROM users GROUP BY ? HAVING id=?"

        self.assertEqual(sql, ex_sql)
        self.assertEqual(args, ['name', 123])

if __name__ == '__main__':
    unittest.main()
