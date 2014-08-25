#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import jsonify

__all__ = ['http_400', 'http_404', 'http_500']

def http_400(exception):
	''' Handles HTTP 400: Bad Request. '''

	response = jsonify({'error' : 'Bad Request', 'exception' : repr(exception)})
	response.status_code = 400
	return response

def http_404(exception):
	''' Handles HTTP 404: Not Found. '''

	response = jsonify({'error' : 'Not Found', 'exception' : repr(exception)})
	response.status_code = 404
	return response

def http_500(exception):
	''' Handles HTTP 500: Internal Server Error. '''

	response = jsonify({'error' : 'Internal Server Error', 'exception' : repr(exception)})
	response.status_code = 500
	return response
