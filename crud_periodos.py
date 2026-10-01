import math
from conexion import Conexion

class CRUDPeriodos:
    def __init__(self):
        self.db = Conexion()

    def calcular_impuesto(self, tipo_empresa, monto_activos, monto_ingresos):
        activos = float(monto_activos)
        ingresos = float(monto_ingresos)
        impuesto = 0.0

        if tipo_empresa == "Natural":
            if ingresos > 1000:
                excedente = ingresos - 1000
                impuesto = excedente * 0.05
        elif tipo_empresa == "Jurídica":
            base = max(activos, ingresos)
            bloques = math.ceil(base / 1000.0)
            impuesto = bloques * 15.00
        elif tipo_empresa == "Gran Contribuyente":
            impuesto = (activos * 0.01) + (ingresos * 0.015)

        return round(impuesto, 2)

    def guardar_periodo(self, datos):
        id_cliente = datos.get('id_cliente')
        
        # 1. Buscar cliente por id_cliente
        sql_cliente = "SELECT tipo_empresa FROM clientes WHERE id_cliente = %s"
        res_cliente = self.db.consultar(sql_cliente, (id_cliente,))

        if not res_cliente:
            return {"error": "Cliente no encontrado"}

        tipo_empresa = res_cliente[0]['tipo_empresa']

        # 2. Calcular impuesto
        monto_impuesto = self.calcular_impuesto(
            tipo_empresa, 
            datos.get('monto_activos', 0), 
            datos.get('monto_ingresos', 0)
        )

        # 3. Insertar registro
        sql = """
            INSERT INTO periodos_impositivos 
            (id_cliente, mes, anio, monto_activos, monto_ingresos, monto_impuesto)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            id_cliente,
            datos.get('mes'),
            datos.get('anio'),
            datos.get('monto_activos', 0),
            datos.get('monto_ingresos', 0),
            monto_impuesto
        )
        res = self.db.ejecutar(sql, valores)

        if res == "ok":
            return {"mensaje": "Período registrado con éxito", "monto_impuesto": monto_impuesto}
        return {"error": res}

    def obtener_historial_periodos(self):
        sql = """
            SELECT p.id_periodo, c.nombre AS nombre_cliente, p.mes, p.anio,
                   p.monto_activos, p.monto_ingresos, p.monto_impuesto
            FROM periodos_impositivos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            ORDER BY p.id_periodo DESC
        """
        return self.db.consultar(sql)