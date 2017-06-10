
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

    def __str__(self):
        out = ""

        if self._select_fields:
            out += "SELECT %s" % ", ".join(self._select_fields)

        elif self.q_count:
            out += "SELECT COUNT(*)"

        out += " FROM %s" % ", ".join(self._source_table)

        if self._offset:
            out += " OFFSET %d" % self._offset

        if self._limit:
            out += " LIMIT %d" % self._limit

        return out


#query = Query().q_from("dildo").q_select("*").q_offset(10).q_limit(20)
query = Query().q_from("dildo").q_count().q_offset(10).q_limit(20)

print(query)
  
