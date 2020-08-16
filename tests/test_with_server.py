# from http.server import HTTPServer, SimpleHTTPRequestHandler
# from socketserver import ThreadingMixIn

# from django_no_sql.db.database import Database

# PATH = 'C:\\Users\\Pende\\Documents\\myapps\\django_no_sql\\db\\database.json'

# database = Database(path_or_url=PATH)
# database.load_database()

# class Requests(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         message = database.manager.all()
#         print(message)
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json; charset=utf-8')
#         self.send_response(200, message=message)
#         self.end_headers()

# class Website(ThreadingMixIn, HTTPServer):
#     pass

# if __name__ == "__main__":
#     server = Website(('127.0.0.1', 4000), Requests)
#     print('Started server at %s' % 'http://127.0.0.1:4000')
#     server.serve_forever()
