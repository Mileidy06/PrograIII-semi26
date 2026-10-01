from conexion import Conexion

class CRUDCliente:
    def __init__(self):
        self.db = Conexion()

    def registrar_cliente(self, datos):
        sql = """
            INSERT INTO clientes (nombre, nit, nrc, tipo_empresa, direccion, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            datos.get('nombre'),
            datos.get('nit'),
            datos.get('nrc'),
            datos.get('tipo_empresa'),
            datos.get('direccion'),
            datos.get('telefono'),
            datos.get('email')
        )
        return self.db.ejecutar(sql, valores)

    def obtener_clientes(self):
        sql = "SELECT * FROM clientes ORDER BY id_cliente DESC"
        return self.db.consultar(sql)

    def buscar_cliente_por_nit(self, nit):
        sql = "SELECT * FROM clientes WHERE nit = %s"
        return self.db.consultar(sql, (nit,))