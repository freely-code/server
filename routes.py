# from tornado import web
# class Test(web.RequestHandler):
#     def get(self):
#         self.write("ok")
from run import MainHandler


class test(MainHandler):

    async def post(self):

        print(self.request.body)
        await self.complete(data="aaa")
