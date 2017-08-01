
class _CommonWhere:
    def __init__(self):
        self._where  = []
        self._where_args = []

    def q_where(self, where_bit, *args):
        self._where.append(where_bit)
        self._where_args.extend(args)
        return self

    def _where_parts(self, out, args):
        if self._where:
            bracketted = [ '(%s)' % s for s in self._where ] 
            anded      = " AND ".join(bracketted)

            out += " WHERE %s" % anded
            args.extend(self._where_args)

        return (out, args)

class Insert:
    def __init__(self):
        self._table = None

    # TODO:
    #  or (rollback, abort, replace, fail, ignore)

    def q_table(self, tab):
        self._table = tab
        self._columns = []
        self._values = []
        return self

    def q_columns(self, *cols):
        self._columns.extend(cols)
        return self
    
    def q_values(self, *val):
        self._values.extend(val)
        return self

    def to_sql(self):
        args = []
        out = "INSERT INTO %s" % self._table
        
        out += " (%s)" % ", ".join(self._columns)
        out += " VALUES (%s)" % ", ".join(['?'] * len(self._columns))
        args.extend(self._values)


        return (out, args)

class Update(_CommonWhere):
    def __init__(self):
        super().__init__()
        self._table = None
        self._set_fields = []
        self._set_args = []

    # TODO:
    #  or (rollback, abort, replace, fail, ignore)

    def q_table(self, tab):
        self._table = tab
        return self
    
    
    def q_set(self, field, value):
        self._set_fields.append(field)
        self._set_args.append(value)
        return self

    def to_sql(self):
        args = []
        out = "UPDATE %s" % self._table

        if len(self._set_fields) > 0:
            set_s = ", ".join(self._set_fields)
            out += " SET %s" % set_s
            args.extend(self._set_args)

        out, args = self._where_parts(out, args)
        return (out, args)


class Delete(_CommonWhere):
    def __init__(self):
        super().__init__()
        self._table = None

    def q_from(self, tab):
        self._table = tab
        return self

    def to_sql(self):
        args = [] 
        sql = "DELETE FROM %s" % self._table

        sql, args = self._where_parts(sql, args)

        return (sql, args)



class Select(_CommonWhere):

    def __init__(self):
        super().__init__()
        self._select_fields = '*'
        #self._count_mode   = False
        self._source_table = None
        #self._distinc = None
        self._join   = None
        self._limit  = None
        self._offset = None
        self._order  = None
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

        # where 
        out, args = self._where_parts(out, args)

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

class Count(Select):
    pass

