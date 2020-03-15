from django_no_sql.db.database import Database
import time

while True:
    database = Database(path_or_url='C:\\Users\\Pende\\Documents\\myapps\\test_flask\\database.json')
    database.load_database()
    products = database.manager.all()
    # product = database.manager.get(name='Hailey')
    print(products.get(name='Kendall'))
    # print(product)
    time.sleep(2)