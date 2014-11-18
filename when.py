import os
import random

from tornado.options import define, options
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, StaticFileHandler, HTTPError

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

define('debug', default=1, help='Debug flag: 1 or 0, 1 by default')

messages_file = os.path.join(os.path.dirname(__file__), 'messages.txt')
messages = {}

# Create a hash table of all commit messages
for line in open(messages_file).readlines():
    messages[md5(line).hexdigest()] = line

class MainHandler(RequestHandler):
    def get(self, message_hash = None):
        if not message_hash:
            message_hash = random.choice(messages.keys())
        elif message_hash not in messages:
            raise HTTPError(404)

        self.output_message(messages[message_hash], message_hash)

    def output_message(self, message, message_hash):
        self.render('index.html', message = message, hash = message_hash)

handlers = [
    (r'/', MainHandler),
    (r'/assets/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'assets')}),
    (r'/([a-z0-9]+)', MainHandler),
]

if __name__ == '__main__':
    options.parse_command_line()

    settings = {
        'debug': options.debug,
    }
    application = Application(handlers, **settings)

    http_server = HTTPServer(application)
    http_server.listen(os.environ.get("PORT", 5000))
    IOLoop.instance().start()
