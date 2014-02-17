#!/usr/bin/python27
 
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
 
import time, os.path
import multiprocessing
import monitor
import config
 
clients = []
 
class ViewHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('views/index.html')
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'New connection'
        clients.append(self)
 
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
        ], static_path = config.static_path
    )

    server = tornado.httpserver.HTTPServer(app)
    server.listen(config.server_port)
    print "Listening on port:", config.server_port
 
    def poll_monitor():
        if not result_queue.empty():
            result = result_queue.get()
            print "Reading: " + str(result)
            for c in clients:
                c.write_message(result)
 
    event_loop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(poll_monitor, 10, io_loop = event_loop)
    scheduler.start()
    event_loop.start()
 
if __name__ == "__main__":
    main()