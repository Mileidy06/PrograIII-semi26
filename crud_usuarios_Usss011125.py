from conexion import DatabaseConnection

class crud_usuarioUsss011125:
    def __init__(self):
        self.db = DatabaseConnection()

    def autenticar(self, usuario, clave):
        sql = """
            SELECT idUsuario, usuario, nombre 
            FROM usuarios_usss011125 
            WHERE usuario = %s AND clave = %s
        """
        resultados = self.db.execute_query(sql, (usuario, clave))
        if resultados:
            return {'status': 'ok', 'usuario': resultados[0]}
        return {'status': 'error', 'msg': 'Acceso denegado: Usuario o contraseña incorrectos'}

    def buscar_usuarios(self, criterio=""):
        sql = """
            SELECT idUsuario, usuario, clave, nombre, direccion, telefono 
            FROM usuarios_usss011125 
            WHERE usuario LIKE %s OR nombre LIKE %s 
            ORDER BY idUsuario DESC
        """
        return self.db.execute_query(sql, (f"%{criterio}%", f"%{criterio}%"))

    def gestionar_usuario(self, datos):
        try:
            accion = datos.get('accion', 'nuevo')

            if accion == 'nuevo':
                sql = """
                    INSERT INTO usuarios_usss011125 (usuario, clave, nombre, direccion, telefono) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                valores = (
                    datos.get('usuario'),
                    datos.get('clave'),
                    datos.get('nombre'),
                    datos.get('direccion'),
                    datos.get('telefono')
                )
                
            elif accion == 'modificar':
                sql = """
                    UPDATE usuarios_usss011125 
                    SET usuario = %s, clave = %s, nombre = %s, direccion = %s, telefono = %s 
                    WHERE idUsuario = %s
                """
                valores = (
                    datos.get('usuario'),
                    datos.get('clave'),
                    datos.get('nombre'),
                    datos.get('direccion'),
                    datos.get('telefono'),
                    datos.get('idUsuario')
                )
                
            elif accion == 'eliminar':
                sql = "DELETE FROM usuarios_usss011125 WHERE idUsuario = %s"
                valores = (datos.get('idUsuario'),)
                
            else:
                return "Acción no reconocida"

            return self.db.execute_statement(sql, valores)
        except Exception as ex:
            return f"Error interno en el servidor: {str(ex)}"