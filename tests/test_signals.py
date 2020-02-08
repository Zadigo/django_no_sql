class Database:
    @classmethod
    def test(cls, func):
        print(func(cls))

@Database.test
def pre_save(func):
    def decorator(self, db_instance=None):
        # func()
        pass
    return decorator

@pre_save
def do_something():
    print('Great')

@pre_save
def another_thing():
    print('Awesome')

d = Database()
