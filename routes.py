from tornado import web
class Test(web.RequestHandler):
    def get(self):
        self.write("ok")
