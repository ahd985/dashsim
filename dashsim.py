import json
import os.path

import tornado.escape
import tornado.ioloop
import tornado.web

from tornado.escape import json_encode
from tornado.options import define, options

class UpdateHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        self._data = data

    def post(self):
        # Use self.write('...') to return html/js/json
        pass


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        self._data = data

    def get(self):
        self.render("dashsim.html", messages=json_encode(self._data))


class DashSim:
    def __init__(self):
        self.cache = {}

    def add_chart(self, chart_id):
        self.cache[chart_id] = {}

    def del_chart(self, chart_id):
        if chart_id in self.cache:
            del self.cache[chart_id]

    # Function completely replaces chart data
    # Consider rewriting to only add what is needed.
    def update_chart_data(self, chart_id, chart_data):
        if chart_id in self.cache:
            self.cache[chart_id] = chart_data

    def start_server(self, port=8888):
        define("port", default=port, help="run on the given port", type=int)
        app = tornado.web.Application(
            [
                (r"/", MainHandler, dict(data=self.cache)),
                (r"/update", UpdateHandler, dict(data=self.cache)),
            ],
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()







