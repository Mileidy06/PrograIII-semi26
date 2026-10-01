CREATE DATABASE IF NOT EXISTS db_sistema_impuestos;
USE db_sistema_impuestos;

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    nit VARCHAR(20),
    nrc VARCHAR(20),
    tipo_empresa VARCHAR(50) NOT NULL,
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100)
);

-- Tabla de productos/actividades económicas
CREATE TABLE IF NOT EXISTS productos (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    activo TINYINT(1) DEFAULT 1
);

INSERT INTO productos (codigo, nombre, activo) VALUES
('11801', 'Comercio General', 1),
('11802', 'Industria y Manufactura', 1)
ON DUPLICATE KEY UPDATE nombre=VALUES(nombre);

-- Tabla de tarifas del impuesto
CREATE TABLE IF NOT EXISTS tarifa_impuesto (
    id_tarifa INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(10) NOT NULL,
    desde DECIMAL(12,2) NOT NULL,
    hasta DECIMAL(12,2) NOT NULL,
    precio_base DECIMAL(12,2) NOT NULL,
    adicional DECIMAL(12,2) NOT NULL,
    porcentaje DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
);

-- Cargar tabla tarifaria
DELETE FROM tarifa_impuesto;
INSERT INTO tarifa_impuesto (codigo_producto, desde, hasta, precio_base, adicional, porcentaje) VALUES
('11801', 0.01, 500.00, 1.50, 0.00, 0.00),
('11801', 500.01, 1000.00, 1.50, 3.00, 0.00),
('11801', 1000.01, 2000.00, 3.00, 3.00, 0.00),
('11801', 2000.01, 3000.00, 6.00, 3.00, 0.00),
('11801', 3000.01, 6000.00, 9.00, 2.00, 0.00),
('11801', 8000.01, 18000.00, 15.00, 2.00, 0.00),
('11801', 18000.01, 30000.00, 39.00, 2.00, 0.00),
('11801', 30000.01, 60000.00, 63.00, 1.00, 0.00),
('11801', 60000.01, 100000.00, 93.00, 0.80, 0.00),
('11801', 100000.01, 200000.00, 125.00, 0.70, 0.00),
('11801', 200000.01, 300000.00, 195.00, 0.60, 0.00),
('11801', 300000.01, 400000.00, 255.00, 0.45, 0.00),
('11801', 400000.01, 500000.00, 300.00, 0.40, 0.00),
('11801', 500000.01, 1000000.00, 340.00, 0.30, 0.00),
('11801', 1000000.01, 99999999.99, 490.00, 0.18, 0.00);

-- Tabla de períodos impositivos registrados
CREATE TABLE IF NOT EXISTS periodos_impositivos (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    codigo_producto VARCHAR(10) NOT NULL,
    fecha_desde DATE NOT NULL,
    fecha_hasta DATE NOT NULL,
    balance DECIMAL(12,2) NOT NULL,
    precio_base DECIMAL(12,2) NOT NULL,
    adicional DECIMAL(12,2) NOT NULL,
    excedente DECIMAL(12,2) NOT NULL,
    bloques INT NOT NULL,
    monto_impuesto DECIMAL(12,2) NOT NULL,
    formula_aplicada VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo)
);