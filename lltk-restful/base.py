#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'Markus Beuckelmann'
__author_email__ = 'email@markus-beuckelmann.de'
__version__ = '0.2.0'

import lltk.exceptions

from flask import Flask
from flask.ext.cache import Cache

from config import config
config['version'] = __version__

app = Flask(config['name'])
cache = Cache(app ,config = {'CACHE_TYPE': 'simple'})

from failure import *

app.register_error_handler(404, http_404)
app.register_error_handler(500, http_500)
app.register_error_handler(TypeError, http_400)
app.register_error_handler(lltk.exceptions.LanguageNotSupported, http_404)
app.register_error_handler(Exception, http_500)

from views import *

if __name__ == '__main__':

	if config['debug']:

		# Run the development server if debug mode is on
		app.run(debug = True, host = config['host'], port = config['port']);
	else:

		try:

			from tornado.wsgi import WSGIContainer
			from tornado.httpserver import HTTPServer
			from tornado.ioloop import IOLoop
			from tornado.log import enable_pretty_logging

			enable_pretty_logging()
			http_server = HTTPServer(WSGIContainer(app))
			http_server.listen(config['port'], config['host'])
			IOLoop.instance().start()

		except ImportError:
			app.run(debug = False, host = config['host'], port = config['port']);
