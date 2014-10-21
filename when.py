import os

from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

class MainHandler(RequestHandler):
    def get(self):
        self.output_message("Hello World!")

    def output_message(self, message):
        self.render('index.html', message = message)

application = Application([
    (r'/', MainHandler),
])

if __name__ == '__main__':
    options.parse_command_line()
    http_server = HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    IOLoop.instance().start()
