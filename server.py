#!/usr/bin/env python

import random
import socket
import time

import drinkz.app


s = socket.socket()
host = socket.gethostname()
port = random.randint(8000, 9999)
s.bind((host, port))

print 'Starting server on', host, port

s.listen(5)
while True:
    c, addr = s.accept()

    print 'GOT CONNECTION FROM', addr

    
    data = c.recv(1024)           # RECEIVE THE GET REQUEST 
    

    path = "".join(data.split())  # FORMAT THE REQUEST FOR SIMPLEAPP()
    path = path[3:-8]             # (take out the GET and HTTP/1.1)
    print path
        
    environ = {}
    environ['PATH_INFO'] = path   # PUT REQUEST INTO THE PATH_INFO

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = drinkz.app.SimpleApp()       #CREATE APP OBJECT
    results = app_obj(environ, my_start_response)

   

    status = d['status']
    headers = d['headers']

    print 'STATUS======  ', status
    print 'HEADERS=====   ', headers
    html = "".join(results)
    
    c.send(status)                # SEND THE STATUS AND THE HTML
    c.send(html)
    
    c.close()
    
