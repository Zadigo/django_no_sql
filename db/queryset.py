from django_no_sql.db.functions import Functions

MAX_VALUES = 3

class EmptyQueryset:
    pass

class QuerySet:
    """
    A queryset represents of individual data retrieved
    from the database regrouped as a single item
    """
    functions = Functions()

    def __init__(self, db_instance=None, query=None):
        if db_instance:
            self.functions.db_data = db_instance.loaded_json_data
        else:
            self.functions.new_queryset = query

    def __repr__(self):
        return str(self.functions.db_data)

    def __str__(self):
        return str(self.functions.new_queryset or self.functions.db_data)

    def __iter__(self):
        return iter(self.functions.new_queryset)

    def copy(self):
        """Creates a fresh QuerySet copy"""
        # if self.functions.has_new_queryset:
        #     klass = self.__class__(query=self.functions.new_queryset)
        # else:
        #     klass = self.__class__(query=self.functions.db_data)
        klass = self.__class__(query=self.functions.new_queryset)
        return klass
