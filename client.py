#!/usr/bin/python27
 
import tornado.platform.twisted
tornado.platform.twisted.install()

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
 
import time, os.path
import multiprocessing
import monitor
import config
import json
import db

clients = []
db.setup()

class ViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('views/index.html')

class DataHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, datatype):
        print datatype
        data = db.last(datatype, 50)
        data.addCallback(self.on_response)

    def on_response(self, data):
        self.write(json.dumps(data))
        self.finish()
        
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'New connection'
        clients.append(self)

    def on_message(self, message):
        print message
        
    def on_close(self):
        print 'Connection closed'
        clients.remove(self)
 
def main():
 
    result_queue = multiprocessing.Queue()
 
    m = monitor.Monitor(result_queue)
    m.daemon = True
    m.start()
 
    # wait a second before sending first task
    time.sleep(1)
    print config.static_path
    app = tornado.web.Application(
        handlers=[
            (r"/", ViewHandler),
            (r"/ws", WebSocketHandler),
            (r"/data/(\w+)", DataHandler)
        ], static_path = config.static_path
    )

    server = tornado.httpserver.HTTPServer(app)
    server.listen(config.server_port)
    print "Listening on port:", config.server_port
 
    def poll_monitor():
        try:
            if not result_queue.empty():
                result = result_queue.get()
                print "Reading: " + str(result)
                for c in clients:
                    c.write_message(json.dumps(result))
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.instance().stop()
 
    event_loop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(poll_monitor, 10, io_loop = event_loop)
    scheduler.start()
    event_loop.current().start()
 
if __name__ == "__main__":
    main()