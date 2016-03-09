import abc
import glob
import json
import os.path
import re

import pandas as pd
import tornado.escape
import tornado.ioloop
import tornado.web

from tornado.escape import json_encode
from tornado.options import define, options

class UpdateHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        self._data = data

    def post(self):
        pass


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, data):
        self._data = data

    def get(self):
        self.render("dashsim.html", messages=json_encode(self._data))


class DashSim:
    def __init__(self):
        self.cache = {}
        self.collector_kwargs = {}

    def add_chart(self, chart_id):
        self.cache[chart_id] = {}

    def del_chart(self, chart_id):
        if chart_id in self.cache:
            del self.cache[chart_id]

    def set_collector(self, collector):
        if not issubclass(collector, DataCollectorMeta):
            raise TypeError('The "collector" input must inherit "DataCollectorMeta" meta class.')

        self.collector = collector

    def call_collector(self):
        if not hasattr(self, 'collector'):
            raise AttributeError('Please provide a data collector class via the "set_collector" class method.')

        self.cache = self.collector.collect_data(self.collector_kwargs)

    # Future implementation
    def set_collector_kwargs(self, collector_kwargs):
        pass

    def start_server(self, port=8888):
        self.call_collector()

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

class DataCollectorMeta(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def collect_data(self, **kwargs):
        """Abstract method that must be implemented for data collection"""
        return

    # Wrapper methods for pandas data readers
    @staticmethod
    def read_csv(*args, **kwargs):
        return pd.read_csv(*args, **kwargs)
    @staticmethod
    def read_excel(*args, **kwargs):
        return pd.read_excel(*args, **kwargs)
    @staticmethod
    def read_json(*args, **kwargs):
        return pd.read_json(*args, **kwargs)
    @staticmethod
    def read_hdf(*args, **kwargs):
        return pd.read_hdf(*args, **kwargs)

    # File searching convenience method
    # Enhance to include more functionality
    @staticmethod
    def find_files(root_dir, extensions, names, include_regex, omit_regex, traverse=True, max_traverse=-1):
        file_list = set()
        root_level = 0

        for root, dirs, files in os.path.walk(root_dir):
            for ext in extensions:
                file_list.update(glob.glob(os.path.join(root,"*." + str(ext))))

            for name in names:
                file_list.update(glob.glob(os.path.join(root,name + "*")))

            for regex in include_regex:
                file_list.update(glob.glob(os.path.join(root,regex)))

            if not traverse:
                break

            if root_level > -1 and root_level >= max_traverse:
                break

            root_level += 1

        # Use omit_regex to filter out any files not wanted
        for regex in omit_regex:
            file_list = [f for f in file_list if not re.match(regex, f) is None]

        return file_list






