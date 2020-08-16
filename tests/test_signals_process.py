class Database:
    def pre_save(self, name):
        def signal(func):
            func(self)
        return signal

    def post_save(self, name):
        def signal(func):
            assert isinstance(func, type)
        return signal

    def load_database(self):
        pass

database = Database()
database.load_database()

@database.pre_save('pre_save')
def test_function(instance):
    print(instance)
