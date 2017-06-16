
class Query:

    def __init__(self):
        self._select_fields = None
        self._count_mode = False
    
    def q_select(self, *fields):
        self._select_fields = fields
        return self

    def q_from(self, *tables):
        self._source_table = tables
        return self
    
    def q_count(self):
        self._count_mode = True
        return self

    def q_limit(self, arg):
        self._limit = arg
        return self

    def q_offset(self, arg):
        self._offset = arg
        return self

    def q_where(self, where_bit, *args):
        self._where = where_bit
        self._where_args = args
        return self

    def to_sql(self):
        out = ""
        args = []

        if self._select_fields:
            out += "SELECT %s" % ", ".join(self._select_fields)

        elif self.q_count:
            out += "SELECT COUNT(*)"

        out += " FROM %s" % ", ".join(self._source_table)

        if self._where:
            out += " WHERE %s" % self._where
            args.extend(self._where_args)

        if self._offset:
            out += " OFFSET %d" % self._offset

        if self._limit:
            out += " LIMIT %d" % self._limit

        return (out, args)


    def __str__(self):
        return "<Query>"

#query = Query().q_from("dildo").q_select("*").q_offset(10).q_limit(20)
_id = 123
query = Query().\
    q_from("dildo").\
    q_count().\
    q_where("id=?", _id).\
    q_offset(10).\
    q_limit(20)

print(query.to_sql())
  
"""

where id=1
where id=1 and a.b = c.d
where id=1 or a.b = c.d
in
like
"""
