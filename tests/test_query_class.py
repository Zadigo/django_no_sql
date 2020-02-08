test = {'name': 'Kendall', 'details': {'age': 15}}

class Query:
    fields = []
    
    def __init__(self, w):
        for key, value in w.items():
            if isinstance(value, dict):
                new_klass = type(f'{key.capitalize()}', (), {'fields': value})
                value = new_klass
            setattr(self, key, value)

    def save(self, db_instance):
        return db_instance.save

    def __setattr__(self, name, value):
        return super().__setattr__(name, value)

# q = Query(test)
# s = q.details
# q.name = 'Hailey'
# print(s)
# # print(s.save)