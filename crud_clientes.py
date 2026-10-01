from conexion import Conexion

class CRUDCliente:
    def __init__(self):
        self.db = Conexion()

    def registrar_cliente(self, datos):
        sql = """
            INSERT INTO clientes (codigo, nombre, nit, nrc, tipo_empresa, direccion, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            datos.get('codigo'),
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

    def obtener_empresas(self):
        sql = "SELECT * FROM clientes WHERE LOWER(tipo_empresa) LIKE '%empresa%' OR LOWER(tipo_empresa) LIKE '%jurídica%' OR LOWER(tipo_empresa) LIKE '%gran%' ORDER BY nombre ASC"
        return self.db.consultar(sql)

    def modificar_cliente(self, id_cliente, datos):
        sql = """
            UPDATE clientes 
            SET codigo = %s, nombre = %s, nit = %s, nrc = %s, tipo_empresa = %s, 
                direccion = %s, telefono = %s, email = %s
            WHERE id_cliente = %s
        """
        valores = (
            datos.get('codigo'),
            datos.get('nombre'),
            datos.get('nit'),
            datos.get('nrc'),
            datos.get('tipo_empresa'),
            datos.get('direccion'),
            datos.get('telefono'),
            datos.get('email'),
            id_cliente
        )
        return self.db.ejecutar(sql, valores)

    def eliminar_cliente(self, id_cliente):
        # Verificar si posee periodos asignados antes de eliminar
        sql_check = "SELECT COUNT(*) as total FROM periodos_impositivos WHERE id_cliente = %s"
        res = self.db.consultar(sql_check, (id_cliente,))
        if res and res[0]['total'] > 0:
            return "No se puede eliminar el cliente porque tiene períodos impositivos registrados."
            
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        return self.db.ejecutar(sql, (id_cliente,))