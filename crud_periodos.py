import math
from datetime import datetime
from conexion import Conexion

class CRUDPeriodos:
    def __init__(self):
        self.db = Conexion()

    def obtener_productos_activos(self):
        sql = "SELECT * FROM productos WHERE activo = 1 ORDER BY nombre ASC"
        return self.db.consultar(sql)

    def calcular_impuesto_tarifa(self, codigo_producto, balance):
        balance = float(balance)
        
        # Consultar el rango tarifario exacto de la BD
        sql = """
            SELECT * FROM tarifa_impuesto 
            WHERE codigo_producto = %s AND %s >= desde AND %s <= hasta
            LIMIT 1
        """
        tarifas = self.db.consultar(sql, (codigo_producto, balance, balance))

        if not tarifas:
            return {"error": f"No se encontró una tarifa aplicable para el balance ${balance:,.2f}"}

        tarifa = tarifas[0]
        precio_base = float(tarifa['precio_base'])
        adicional = float(tarifa['adicional'])
        desde = float(tarifa['desde'])
        
        excedente = max(0.0, balance - (desde - 0.01))
        bloques = math.ceil(excedente / 1000.0) if (adicional > 0 and excedente > 0) else 0
        
        monto_impuesto = precio_base + (bloques * adicional)
        
        if bloques > 0:
            formula = f"${precio_base:.2f} base + ({bloques} bloques x ${adicional:.2f})"
        else:
            formula = f"${precio_base:.2f} base fija"

        return {
            "precio_base": precio_base,
            "adicional": adicional,
            "excedente": excedente,
            "bloques": bloques,
            "monto_impuesto": round(monto_impuesto, 2),
            "formula": formula
        }

    def guardar_periodo(self, datos):
        id_cliente = datos.get('id_cliente')
        codigo_producto = datos.get('codigo_producto')
        fecha_desde = datos.get('fecha_desde')
        fecha_hasta = datos.get('fecha_hasta')
        balance = float(datos.get('balance', 0))

        # Validaciones de Fechas
        if fecha_desde >= fecha_hasta:
            return {"error": "La fecha 'Desde' debe ser anterior a la fecha 'Hasta'."}

        # Validar Superposición de Períodos para el mismo cliente
        sql_overlap = """
            SELECT COUNT(*) as total FROM periodos_impositivos
            WHERE id_cliente = %s AND NOT (fecha_hasta < %s OR fecha_desde > %s)
        """
        res_overlap = self.db.consultar(sql_overlap, (id_cliente, fecha_desde, fecha_hasta))
        if res_overlap and res_overlap[0]['total'] > 0:
            return {"error": "El cliente ya tiene un período registrado que se superpone con este rango de fechas."}

        # Calcular
        calc = self.calcular_impuesto_tarifa(codigo_producto, balance)
        if "error" in calc:
            return calc

        # Insertar Período
        sql = """
            INSERT INTO periodos_impositivos 
            (id_cliente, codigo_producto, fecha_desde, fecha_hasta, balance, precio_base, adicional, excedente, bloques, monto_impuesto, formula_aplicada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            id_cliente,
            codigo_producto,
            fecha_desde,
            fecha_hasta,
            balance,
            calc['precio_base'],
            calc['adicional'],
            calc['excedente'],
            calc['bloques'],
            calc['monto_impuesto'],
            calc['formula']
        )
        res = self.db.ejecutar(sql, valores)

        if res == "ok":
            return {"mensaje": "Período guardado e historial congelado con éxito", "calculo": calc}
        return {"error": res}

    def obtener_historial_periodos(self):
        sql = """
            SELECT p.id_periodo, c.nombre AS nombre_cliente, prod.nombre AS producto,
                   p.fecha_desde, p.fecha_hasta, p.balance, p.monto_impuesto, p.formula_aplicada
            FROM periodos_impositivos p
            INNER JOIN clientes c ON p.id_cliente = c.id_cliente
            INNER JOIN productos prod ON p.codigo_producto = prod.codigo
            ORDER BY p.id_periodo DESC
        """
        return self.db.consultar(sql)