import os

from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler

class MainHandler(RequestHandler):
    def get(self, message = None):
        self.output_message(message)

    def output_message(self, message):
        self.render('index.html', message = message)

settings = {
    'debug': True,
}

handlers = [
    (r'/', MainHandler),
    (r'/assets/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'assets')}),
    (r'/([a-z0-9]+)', MainHandler),
]

application = Application(handlers, **settings)

if __name__ == '__main__':
    options.parse_command_line()
    http_server = HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    IOLoop.instance().start()
