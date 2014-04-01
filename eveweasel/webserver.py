from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

from eveweasel.application import EveWeasel

def run_server():
    weasel = EveWeasel()

    application = Application(weasel.get_paths())

    application.listen(weasel.config['port'])
    application.weasel = weasel
    print("Starting server on port %s" % weasel.config['port'])
    IOLoop.instance().start()
    

if __name__ == '__main__':
    run_server()
 
