from django_no_sql.db.functions import Functions

MAX_VALUES = 3

class QuerySet:
    functions = Functions()

    def __init__(self, db_instance=None, query=None):
        if db_instance:
            self.functions.db_data = db_instance.loaded_json_data
        else:
            self.functions.new_queryset = query

    def __repr__(self):
        return str(self.functions.db_data) 

    def copy(self):
        klass = self.__class__(query=self.functions.new_queryset)
        return klass
