from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http.cookies import SimpleCookie
from helpers import *
from mongo import MongoDatabase
import cgi
from urllib.parse import parse_qs
import json

class LMSRequestHandler(BaseHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        self.db = MongoDatabase()        
        self.db.connect()
        super().__init__(*args,**kwargs)

    def _POST(method,*args,**kwargs):
        def main(self,*args,**kwargs):
            if self.path.startswith('/api/'):
                return method(self,*args,**kwargs)
            #do something
            self.POST = {}
            ctype , pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'],'utf-8')
                fields = cgi.parse_multipart(self.rfile,pdict=pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.get('content-length'))
                fields = parse_qs(self.rfile.read(length).decode(),keep_blank_values="blank")
            for key in fields:
                self.POST[key] = fields[key][0]
            return method(self,*args,**kwargs)
        return main
    def do_GET(self):
        self.path = self.path.removesuffix("/")
        if self.path == "/":

            self.render('user_login.html')
        
        elif self.path == "/libadmin/login":

            self.render('libadmin_login.html')

        elif self.path == '/libadmin/dashboard/':

            self.render('libadmin_dashboard.html')
        
        elif self.path == '/libadmin/bookmanager':

            self.render('book_management.html')

        elif self.path == '/user/signup' :
            
            self.render('user_signup.html')

        elif self.path == '/user/login':

            self.render('user_login.html')

        else:
            self.render_html("<html><body><h1>Please enter a Valid URL </h1></body></html>")

    @_POST
    def do_POST(self):
        self.path = self.path.removesuffix("/")
        if self.path == '/user/signup':
            self.db.create_user(self.POST)
            self.render("user_login.html")
        # elif self.path == /user/login/'

    

    def send_json_response(self,response_dict:dict=None):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_dict).encode())
    def render(self,template:str,alert:str=False,status:int=None,context:dict=None,cookies=None):
        with open(f'templates/{template}','r') as template:
            htmlresponse = template.read()
        if context:
            for key in context:
                tag = "{% " + key + " %}"
                htmlresponse = htmlresponse.replace(tag,str(context[key]))
        if alert: htmlresponse += f"<script>alert('{alert}');</script>"
        if status:self.send_response(status)
        else:self.send_response(200)
        self.send_header('Content-type','text/html')
        if cookies:
            cookie_obj = SimpleCookie()
            for cookie_name , cookie_value in cookies.items():
                cookie_obj[cookie_name] = cookie_value
            for morsel in cookie_obj.values():
                morsel['path'] = '/'
                self.send_header("Set-Cookie", morsel.OutputString())
        self.end_headers()
        self.wfile.write(htmlresponse.encode())
    def render_html(self,html_response,status=None):
        if status == None:self.send_response(200)
        else : self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(html_response.encode())
    def redirect(self,url:str,cookies:dict=None):
        self.send_response(301)
        if cookies:
            cookie_obj = SimpleCookie()
            for cookie_name , cookie_value in cookies.items():
                cookie_obj[cookie_name] = cookie_value
            for morsel in cookie_obj.values():
                morsel['path'] = '/'
                self.send_header("Set-Cookie", morsel.OutputString())
        self.send_header('Location',url)
        self.end_headers()
def main(host:str='127.0.0.1',port:int=8000) -> None:
    server = HTTPServer((host,port),RequestHandlerClass=LMSRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n Server closed. \n")

if __name__ == "__main__":
    main()