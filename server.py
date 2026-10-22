from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

import crud_usuarios_Usss011125

PORT = 3000
controlador = crud_usuarios_Usss011125.crud_usuarioUsss011125()

class AppServerHandler(SimpleHTTPRequestHandler):
    def _enviar_json(self, payload, code=200):
        body = json.dumps(payload, default=str).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            path = urlparse(self.path).path

            # Aceptamos tanto /login como rutas vacías o /login.html por seguridad
            if path in ['/login', '/login.html', '/']:
                usuario = data.get('usuario')
                clave = data.get('clave')
                resultado = controlador.autenticar(usuario, clave)
                self._enviar_json(resultado)
                return

            if path == '/usuario':
                resultado = controlador.gestionar_usuario(data)
                self._enviar_json({'msg': resultado})
                return

            self._enviar_json({'msg': 'Ruta POST no encontrada'}, 404)
        except Exception as err:
            self._enviar_json({'msg': f'Error del servidor: {err}'}, 500)

    def do_GET(self):
        try:
            parsed_url = urlparse(self.path)
            params = parse_qs(parsed_url.query)

            if parsed_url.path == '/usuario':
                criterio = params.get('buscar', [''])[0]
                registros = controlador.buscar_usuarios(criterio)
                self._enviar_json(registros)
                return

            if parsed_url.path == '/' or parsed_url.path == '/login':
                self.path = '/login.html'
                return SimpleHTTPRequestHandler.do_GET(self)

            if parsed_url.path == '/sistema':
                self.path = '/index.html'
                return SimpleHTTPRequestHandler.do_GET(self)

            return SimpleHTTPRequestHandler.do_GET(self)
        except Exception as err:
            self._enviar_json({'msg': f'Error del servidor: {err}'}, 500)

if __name__ == '__main__':
    servidor = HTTPServer(('localhost', PORT), AppServerHandler)
    print(f'Servidor ejecutándose exitosamente en http://localhost:{PORT}')
    servidor.serve_forever()