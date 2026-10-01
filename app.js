const API_URL = 'http://localhost:3000';

document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
    cargarHistorialPeriodos();

    const formCliente = document.getElementById('formCliente');
    if (formCliente) {
        formCliente.addEventListener('submit', guardarCliente);
    }

    const formImpuesto = document.getElementById('formImpuesto');
    if (formImpuesto) {
        formImpuesto.addEventListener('submit', calcularYGuardarImpuesto);
    }
});

// Cargar lista de clientes para la tabla y el select del formulario
async function cargarClientes() {
    try {
        const response = await fetch(`${API_URL}/clientes`);
        const clientes = await response.json();

        // 1. Llenar Select del Formulario
        const selectCliente = document.getElementById('selectCliente');
        if (selectCliente) {
            selectCliente.innerHTML = '<option value="">Seleccione un cliente...</option>';
            clientes.forEach(cliente => {
                const option = document.createElement('option');
                // Se asigna prioritariamente el ID numérico
                const idCliente = cliente.id_cliente !== undefined ? cliente.id_cliente : cliente.id;
                option.value = idCliente;
                option.textContent = `${cliente.nombre} (${cliente.nit || 'Sin NIT'})`;
                selectCliente.appendChild(option);
            });
        }

        // 2. Llenar Tabla de Clientes
        const tablaBody = document.getElementById('tablaClientesBody');
        if (tablaBody) {
            tablaBody.innerHTML = '';
            clientes.forEach(cliente => {
                const idCliente = cliente.id_cliente !== undefined ? cliente.id_cliente : cliente.id;
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${idCliente}</td>
                    <td>${cliente.nombre}</td>
                    <td>${cliente.nit || '-'}</td>
                    <td>${cliente.tipo_empresa || '-'}</td>
                    <td>${cliente.email || '-'}</td>
                `;
                tablaBody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error al cargar clientes:', error);
    }
}

// Cargar historial de períodos calculados
async function cargarHistorialPeriodos() {
    try {
        const response = await fetch(`${API_URL}/periodos`);
        const periodos = await response.json();

        const tablaBody = document.getElementById('tablaPeriodosBody');
        if (tablaBody) {
            tablaBody.innerHTML = '';
            periodos.forEach(p => {
                const idPeriodo = p.id_periodo !== undefined ? p.id_periodo : p.id;
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${idPeriodo}</td>
                    <td>${p.nombre_cliente || p.cliente || '-'}</td>
                    <td>${p.mes}/${p.anio}</td>
                    <td>$${parseFloat(p.monto_activos || 0).toFixed(2)}</td>
                    <td>$${parseFloat(p.monto_ingresos || 0).toFixed(2)}</td>
                    <td class="fw-bold text-success">$${parseFloat(p.impuesto_calculado || p.impuesto || 0).toFixed(2)}</td>
                `;
                tablaBody.appendChild(row);
            });
        }
    } catch (error) {
        console.error('Error al cargar historial:', error);
    }
}

// Guardar nuevo cliente
async function guardarCliente(event) {
    event.preventDefault();

    const data = {
        nombre: document.getElementById('nombre').value,
        nit: document.getElementById('nit').value,
        nrc: document.getElementById('nrc').value,
        tipo_empresa: document.getElementById('tipo_empresa').value,
        direccion: document.getElementById('direccion').value,
        telefono: document.getElementById('telefono').value,
        email: document.getElementById('email').value
    };

    try {
        const response = await fetch(`${API_URL}/cliente`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const res = await response.json();
        if (res.error) {
            alert('Error: ' + res.error);
        } else {
            alert('Cliente guardado exitosamente');
            document.getElementById('formCliente').reset();
            cargarClientes();
        }
    } catch (error) {
        console.error('Error al guardar cliente:', error);
    }
}

// Calcular y guardar impuesto del período
async function calcularYGuardarImpuesto(event) {
    event.preventDefault();

    const selectCliente = document.getElementById('selectCliente');
    const id_cliente = parseInt(selectCliente.value, 10);

    if (!id_cliente) {
        alert('Por favor seleccione un cliente válido.');
        return;
    }

    const data = {
        id_cliente: id_cliente,
        mes: parseInt(document.getElementById('mes').value, 10),
        anio: parseInt(document.getElementById('anio').value, 10),
        monto_activos: parseFloat(document.getElementById('monto_activos').value) || 0,
        monto_ingresos: parseFloat(document.getElementById('monto_ingresos').value) || 0
    };

    try {
        const response = await fetch(`${API_URL}/periodo/calcular`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const res = await response.json();
        if (res.error) {
            alert('Error: ' + res.error);
        } else {
            alert('Impuesto calculado y registrado con éxito');
            document.getElementById('formImpuesto').reset();
            cargarHistorialPeriodos();
        }
    } catch (error) {
        console.error('Error al calcular el impuesto:', error);
    }
}