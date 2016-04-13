# encoding: utf-8

import tornado.ioloop
import tornado.web
from jinja2 import Environment, FileSystemLoader
import requests
import tornado.options
import os

TEMPLATE_FILE = "board.html"


class MainHandler(tornado.web.RequestHandler):
    static_directory = "../static"
    templateEnv = Environment(static_directory, loader=FileSystemLoader(searchpath="templates"))
    template = templateEnv.get_template(TEMPLATE_FILE)

    def get(self):
        username = 'juliana.goncalves@corp.globo.com'
        password = 'Admin1234'
        url_api = "https://produtos-globocom.leankit.com/kanban/api/board/196166479/archive"

        http = requests.Session()
        http.auth = (username, password)
        response = http.get(url_api).json()  # dicionario pythonn

        board_datas = response

        cards_esp2 = board_datas['ReplyData'][0][0]['ChildLanes'][2]['Lane']['Cards']

        title = board_datas['ReplyData'][0][0]['ChildLanes'][2]['Lane']['Title']

        html_output = self.template.render(title=title, cards=cards_esp2)
        self.write(html_output)

        self.finish()

# def make_app():
#     return tornado.web.Application([
#         (r"/", MainHandler),  # mapeamento url
#     ])

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = {
            "debug": True,
            "static_path": os.path.join(os.path.dirname(__file__), "static")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
