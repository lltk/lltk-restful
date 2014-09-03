#!/usr/bin/python
# -*- coding: UTF-8 -*-

import lltk
import lltk.generic
import lltk.caching
import lltk.exceptions
from hashlib import md5

from flask import jsonify, request

from base import app, cache, config
from failure import *

if config['debug']:
	lltk.config['debug'] = True
if config['caching']:
	lltk.caching.enable()

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
		try:
			data['result'] = function(language, word, *extraargs, **kwargs)
		except TypeError:
			data['result'] = function(language, word, *extraargs)
	else:
		return http_404(NotImplementedError)

	return jsonify(data)

@app.route('/lltk/translate/<string:src>/<string:dest>/<string:word>', methods = ['GET'])
@app.route('/lltk/translate/<string:src>/<string:dest>/<path:extraargs>/<string:word>', methods = ['GET'])
@cache.cached(timeout = 300, key_prefix = lambda: md5(repr(request)).hexdigest(), unless = lambda: bool(request.args.has_key('caching') and request.args['caching'].lower() == 'false'))
def translate(src, dest, word, extraargs = tuple(), methods = ['GET']):
	''' Returns translate() results as a JSON document. '''

	data = dict()
	data['language'] = dest
	data['language-from'] = src
	data['language-to'] = dest
	data['method'] = 'translate'
	data['word'] = word
	data['result'] = None

	if not isinstance(extraargs, tuple):
		extraargs = tuple(extraargs.split('/'))
	kwargs = request.args.to_dict()

	data['result'] = lltk.generic.translate(src, dest, word, *extraargs, **kwargs)

	return jsonify(data)

@app.route('/lltk/info', methods = ['GET'])
def info():

	data = dict()
	data['server'] = 'Language Learning Toolkit ResRESTful API'
	data['version'] = config['version']
	data['lltk-version'] = lltk.config['version']
	return jsonify(data)
