
#class _Common:
#    pass

class Insert:
    pass

class Update:
    pass

class Delete:
    pass


class Count:
    pass

class Select:

    def __init__(self):
        self._select_fields = '*'
        self._count_mode   = False
        self._source_table = None
        #self._distinc = None
        self._join   = None
        self._limit  = None
        self._offset = None
        self._order  = None
        self._where  = []
        self._where_args = []
        self._group = None
        self._group_having = None
        self._group_args = []

    def one(self):
        self._limit = 1
        self.as_one_record = True
        return self
    
    def q_select(self, *fields):
        self._select_fields = fields
        return self

    # this can be done as a select fields
    #def q_distinct(self, arg):
    #    self._distinct = arg
    #    return self

    def q_from(self, *tables):
        self._source_table = tables
        return self

    def q_join(self, table, join_on):
        self._join = table
        self._join_on = join_on
        return self
    
    def q_group_by(self, grp, having = None, *having_args):
        self._group = grp
        self._group_having = having
        self._group_args = having_args
        return self

    #def q_count(self):
    #    self._count_mode = True
    #    return self

    def q_limit(self, arg):
        self._limit = arg
        return self

    def q_offset(self, arg):
        self._offset = arg
        return self

    def q_order_by(self, args):
        self._order = args
        return self

    def q_where(self, where_bit, *args):
        self._where.append(where_bit)
        self._where_args.extend(args)
        return self

    def to_sql(self):
        out = ""
        args = []

        if self._select_fields:
            out += "SELECT %s" % ", ".join(self._select_fields)

        #elif self.q_count:
        #    out += "SELECT COUNT(*)"


        out += " FROM %s" % ", ".join(self._source_table)

        if self._join:
            out += " JOIN %s ON %s" % (self._join, self._join_on)

        if self._where:
            bracketted = [ '(%s)' % s for s in self._where ] 
            anded      = " AND ".join(bracketted)

            out += " WHERE %s" % anded
            args.extend(self._where_args)

        if self._group:
            out += " GROUP BY ?"
            args.append(self._group)

            if self._group_having:
                out += " HAVING %s" % self._group_having
                args.extend(self._group_args)

        if self._order:
            out += " ORDER BY %s" % self._order


        if self._offset:
            out += " OFFSET ?"
            args.append(self._offset)

        if self._limit:
            out += " LIMIT ?"
            args.append(self._limit)

        return (out, args)


    def __str__(self):
        return "<Query>"

#query = Query().q_from("dildo").q_select("*").q_offset(10).q_limit(20)
#_id = 123
#query = Select().\
#    one().\
#    q_from("dildo").\
#    q_count().\
#    q_where("id=?", _id).\
#    q_offset(10)

#print(query.to_sql())
  
"""

where id=1
where id=1 and a.b = c.d
where id=1 or a.b = c.d
in
like
"""
