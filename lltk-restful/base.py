#!/usr/bin/python
# -*- coding: UTF-8 -*-

import lltk
import lltk.generic
import lltk.caching
import lltk.exceptions

from flask import Flask
from flask import jsonify, request
from flask.ext.cache import Cache
from hashlib import md5

from failure import *

__author__ = 'Markus Beuckelmann'
__author_email__ = 'email@markus-beuckelmann.de'
__version__ = '0.1.0'

DEBUG = True
CACHING = True
NAME = 'lltk-restful'
HOST = '127.0.0.1'
PORT = 5000

app = Flask(NAME)
cache = Cache(app ,config = {'CACHE_TYPE': 'simple'})

app.register_error_handler(404, http_404)
app.register_error_handler(500, http_500)
app.register_error_handler(TypeError, http_400)
app.register_error_handler(lltk.exceptions.LanguageNotSupported, http_404)
app.register_error_handler(Exception, http_500)

if DEBUG:
	app.debug = True
	lltk.config['debug'] = True
if not CACHING:
	lltk.caching.disable()

@app.route('/lltk/<string:language>/<string:method>/<string:word>', methods = ['GET'])
@app.route('/lltk/<string:language>/<string:method>/<path:extraargs>/<string:word>', methods = ['GET'])
@cache.cached(timeout = 3600, key_prefix = lambda: md5(repr(request)).hexdigest(), unless = lambda: bool(request.args.has_key('caching') and request.args['caching'].lower() == 'false'))
def lltkapi(language, method, word, extraargs = tuple()):
	''' Returns LLTK's results as a JSON document. '''

	data = dict()
	data['language'] = language
	data['method'] = method
	data['word'] = word
	data['result'] = None

	if hasattr(lltk.generic, method) and callable(getattr(lltk.generic, method)):
		function = getattr(lltk.generic, method)
		if not isinstance(extraargs, tuple):
			extraargs = tuple(extraargs.split('/'))
		kwargs = request.args.to_dict()
		data['result'] = function(language, word, *extraargs, **kwargs)
	else:
		return http_404(NotImplementedError)

	return jsonify(data)

@app.route('/lltk/info', methods = ['GET'])
def info():

	data = dict()
	data['server'] = 'Language Learning Toolkit ResRESTful API'
	data['version'] = __version__
	data['lltk-version'] = lltk.config['version']
	return jsonify(data)

if __name__ == '__main__':

	app.run(
		host = HOST,
		port = PORT
	)
