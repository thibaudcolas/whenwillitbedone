import os
import random

from tornado.options import options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

messages_file = os.path.join(os.path.dirname(__file__), 'messages.txt')
messages = {}

# Create a hash table of all commit messages
for line in open(messages_file).readlines():
    messages[md5(line).hexdigest()] = line

class MainHandler(RequestHandler):
    def get(self, message = None):
        message_hash = random.choice(messages.keys())
        self.output_message(messages[message_hash])

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
