-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-10-2026 a las 06:10:32
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_sistema_impuestos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `nit` varchar(20) DEFAULT NULL,
  `nrc` varchar(20) DEFAULT NULL,
  `tipo_empresa` varchar(50) NOT NULL,
  `direccion` text DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `codigo`, `nombre`, `nit`, `nrc`, `tipo_empresa`, `direccion`, `telefono`, `email`) VALUES
(1, 'CLI-001', 'Comercial San Miguel S.A. de C.V.', '0614-150820-101-3', '123456-7', 'Empresa Jurídica', 'San Miguel', '2222-3333', 'sanmiguel@gmail.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `periodos_impositivos`
--

CREATE TABLE `periodos_impositivos` (
  `id_periodo` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `codigo_producto` varchar(10) NOT NULL,
  `fecha_desde` date NOT NULL,
  `fecha_hasta` date NOT NULL,
  `balance` decimal(12,2) NOT NULL,
  `precio_base` decimal(12,2) NOT NULL,
  `adicional` decimal(12,2) NOT NULL,
  `excedente` decimal(12,2) NOT NULL,
  `bloques` int(11) NOT NULL,
  `monto_impuesto` decimal(12,2) NOT NULL,
  `formula_aplicada` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `periodos_impositivos`
--

INSERT INTO `periodos_impositivos` (`id_periodo`, `id_cliente`, `codigo_producto`, `fecha_desde`, `fecha_hasta`, `balance`, `precio_base`, `adicional`, `excedente`, `bloques`, `monto_impuesto`, `formula_aplicada`) VALUES
(1, 1, '11801', '2026-01-01', '2026-01-31', 550000.00, 340.00, 0.30, 50000.00, 50, 355.00, '$340.00 base + (50 bloques x $0.30)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `codigo` varchar(10) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`codigo`, `nombre`, `activo`) VALUES
('11801', 'Comercio General', 1),
('11802', 'Industria y Manufactura', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifa_impuesto`
--

CREATE TABLE `tarifa_impuesto` (
  `id_tarifa` int(11) NOT NULL,
  `codigo_producto` varchar(10) NOT NULL,
  `desde` decimal(12,2) NOT NULL,
  `hasta` decimal(12,2) NOT NULL,
  `precio_base` decimal(12,2) NOT NULL,
  `adicional` decimal(12,2) NOT NULL,
  `porcentaje` decimal(5,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tarifa_impuesto`
--

INSERT INTO `tarifa_impuesto` (`id_tarifa`, `codigo_producto`, `desde`, `hasta`, `precio_base`, `adicional`, `porcentaje`) VALUES
(1, '11801', 0.01, 500.00, 1.50, 0.00, 0.00),
(2, '11801', 500.01, 1000.00, 1.50, 3.00, 0.00),
(3, '11801', 1000.01, 2000.00, 3.00, 3.00, 0.00),
(4, '11801', 2000.01, 3000.00, 6.00, 3.00, 0.00),
(5, '11801', 3000.01, 6000.00, 9.00, 2.00, 0.00),
(6, '11801', 8000.01, 18000.00, 15.00, 2.00, 0.00),
(7, '11801', 18000.01, 30000.00, 39.00, 2.00, 0.00),
(8, '11801', 30000.01, 60000.00, 63.00, 1.00, 0.00),
(9, '11801', 60000.01, 100000.00, 93.00, 0.80, 0.00),
(10, '11801', 100000.01, 200000.00, 125.00, 0.70, 0.00),
(11, '11801', 200000.01, 300000.00, 195.00, 0.60, 0.00),
(12, '11801', 300000.01, 400000.00, 255.00, 0.45, 0.00),
(13, '11801', 400000.01, 500000.00, 300.00, 0.40, 0.00),
(14, '11801', 500000.01, 1000000.00, 340.00, 0.30, 0.00),
(15, '11801', 1000000.01, 99999999.99, 490.00, 0.18, 0.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios_usss011125`
--

CREATE TABLE `usuarios_usss011125` (
  `idUsuario` int(10) NOT NULL,
  `usuario` varchar(35) NOT NULL,
  `clave` varchar(35) NOT NULL,
  `nombre` varchar(85) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  `telefono` varchar(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `codigo` (`codigo`);

--
-- Indices de la tabla `periodos_impositivos`
--
ALTER TABLE `periodos_impositivos`
  ADD PRIMARY KEY (`id_periodo`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `codigo_producto` (`codigo_producto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`codigo`);

--
-- Indices de la tabla `tarifa_impuesto`
--
ALTER TABLE `tarifa_impuesto`
  ADD PRIMARY KEY (`id_tarifa`),
  ADD KEY `codigo_producto` (`codigo_producto`);

--
-- Indices de la tabla `usuarios_usss011125`
--
ALTER TABLE `usuarios_usss011125`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `periodos_impositivos`
--
ALTER TABLE `periodos_impositivos`
  MODIFY `id_periodo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `tarifa_impuesto`
--
ALTER TABLE `tarifa_impuesto`
  MODIFY `id_tarifa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `usuarios_usss011125`
--
ALTER TABLE `usuarios_usss011125`
  MODIFY `idUsuario` int(10) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `periodos_impositivos`
--
ALTER TABLE `periodos_impositivos`
  ADD CONSTRAINT `periodos_impositivos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `periodos_impositivos_ibfk_2` FOREIGN KEY (`codigo_producto`) REFERENCES `productos` (`codigo`);

--
-- Filtros para la tabla `tarifa_impuesto`
--
ALTER TABLE `tarifa_impuesto`
  ADD CONSTRAINT `tarifa_impuesto_ibfk_1` FOREIGN KEY (`codigo_producto`) REFERENCES `productos` (`codigo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
