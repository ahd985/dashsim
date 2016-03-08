import tornado.escape
import tornado.ioloop
import tornado.web
import os.path

from tornado.options import define, options, parse_command_line


class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        # Use self.write('...') to return html/js/json
        pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dashsim.html", messages=[])


def start_server(port=8888):
    define("port", default=port, help="run on the given port", type=int)
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/update", UpdateHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


