import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse
from .__main__ import ROOT,examples
from .engine import suite
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*_):pass
    def reply(self,code,data,kind='application/json'):
        content=data if isinstance(data,bytes) else json.dumps(data).encode();self.send_response(code);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('Content-Length',str(len(content)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(content)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/published-evidence':
            evidence=ROOT/'examples/three-engine-evidence.json'
            return self.reply(200,json.loads(evidence.read_text())) if evidence.exists() else self.reply(404,{'error':'not_found'})
        if path in ('/','/app.js','/style.css'):
            file='index.html' if path=='/' else path[1:];return self.reply(200,(ROOT/'web'/file).read_bytes(),{'index.html':'text/html','app.js':'text/javascript','style.css':'text/css'}[file])
        self.reply(404,{'error':'not_found'})
    def do_POST(self):
        if self.path!='/api/run':return self.reply(404,{'error':'not_found'})
        if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{self.server.server_port}'):return self.reply(403,{'error':'origin_denied'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=50000:raise ValueError('size')
            body=json.loads(self.rfile.read(size));indices=body.get('case_indices',[0,1,2,3])
            if not isinstance(indices,list) or not 1<=len(indices)<=4 or any(type(i)is not int or not 0<=i<4 for i in indices):raise ValueError('cases')
            self.reply(200,suite([examples()[i] for i in indices],('sqlite_fts5',)))
        except (ValueError,TypeError,KeyError):self.reply(400,{'error':'invalid_input','messages':['Entrée non valide','Invalid input','Entrada no válida']})
def serve(port=8772):ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
