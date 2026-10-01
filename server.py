from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import urlparse

from crud_clientes import CRUDCliente
from crud_periodos import CRUDPeriodos

crud_cliente = CRUDCliente()
crud_periodo = CRUDPeriodos()

class CustomRequestHandler(SimpleHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/clientes':
            clientes = crud_cliente.obtener_clientes()
            self._set_headers(200)
            self.wfile.write(json.dumps(clientes, default=str).encode('utf-8'))

        elif path == '/periodos':
            periodos = crud_periodo.obtener_historial_periodos()
            self._set_headers(200)
            self.wfile.write(json.dumps(periodos, default=str).encode('utf-8'))

        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except json.JSONDecodeError:
            data = {}

        if path == '/cliente':
            resultado = crud_cliente.registrar_cliente(data)
            self._set_headers(200)
            respuesta = {"mensaje": "Cliente registrado correctamente"} if resultado == "ok" else {"error": resultado}
            self.wfile.write(json.dumps(respuesta).encode('utf-8'))

        elif path == '/periodo/calcular':
            resultado = crud_periodo.guardar_periodo(data)
            self._set_headers(200)
            self.wfile.write(json.dumps(resultado).encode('utf-8'))

        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Ruta no encontrada"}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor corriendo en http://localhost:{port}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
        httpd.server_close()

if __name__ == '__main__':
    run()