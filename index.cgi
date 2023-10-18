#!/usr/local/bin/python3.4
from wsgiref.handlers import CGIHandler
#from flaskSample import app -- 20220820edit nishibe
from index import app
CGIHandler().run(app)