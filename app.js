const API_URL = 'http://localhost:3000';

document.addEventListener('DOMContentLoaded', () => {
    cargarClientes();
    cargarEmpresasSelect();
    cargarProductosSelect();
    cargarHistorialPeriodos();

    document.getElementById('formCliente').addEventListener('submit', guardarCliente);
    document.getElementById('formImpuesto').addEventListener('submit', guardarPeriodo);
});

// ==================== SECCIÓN CLIENTES (CRUD COMPLETO) ====================

async function cargarClientes() {
    try {
        const response = await fetch(`${API_URL}/clientes`);
        const clientes = await response.json();
        const tbody = document.getElementById('tablaClientesBody');
        tbody.innerHTML = '';

        clientes.forEach(c => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="badge bg-secondary">${c.codigo}</span></td>
                <td class="fw-bold">${c.nombre}</td>
                <td>${c.nit || '-'}</td>
                <td><span class="badge bg-info text-dark">${c.tipo_empresa}</span></td>
                <td class="small">${c.email || '-'}<br>${c.telefono || ''}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-warning me-1" onclick="editarCliente(${JSON.stringify(c).replace(/"/g, '&quot;')})"><i class="fa-solid fa-pen"></i></button>
                    <button class="btn btn-sm btn-outline-danger" onclick="eliminarCliente(${c.id_cliente})"><i class="fa-solid fa-trash"></i></button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al cargar clientes:', error);
    }
}

async function guardarCliente(e) {
    e.preventDefault();

    const id_edit = document.getElementById('cliente_id_edit').value;
    const data = {
        id_cliente: id_edit ? parseInt(id_edit) : null,
        codigo: document.getElementById('codigo').value,
        nombre: document.getElementById('nombre').value,
        nit: document.getElementById('nit').value,
        nrc: document.getElementById('nrc').value,
        tipo_empresa: document.getElementById('tipo_empresa').value,
        direccion: document.getElementById('direccion').value,
        telefono: document.getElementById('telefono').value,
        email: document.getElementById('email').value
    };

    const endpoint = id_edit ? `${API_URL}/cliente/modificar` : `${API_URL}/cliente`;

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const res = await response.json();

        if (res.error) {
            alert('Error: ' + res.error);
        } else {
            alert(res.mensaje);
            limpiarFormCliente();
            cargarClientes();
            cargarEmpresasSelect();
        }
    } catch (error) {
        console.error('Error al guardar cliente:', error);
    }
}

function editarCliente(c) {
    document.getElementById('cliente_id_edit').value = c.id_cliente;
    document.getElementById('codigo').value = c.codigo;
    document.getElementById('nombre').value = c.nombre;
    document.getElementById('nit').value = c.nit;
    document.getElementById('nrc').value = c.nrc;
    document.getElementById('tipo_empresa').value = c.tipo_empresa;
    document.getElementById('direccion').value = c.direccion;
    document.getElementById('telefono').value = c.telefono;
    document.getElementById('email').value = c.email;

    document.getElementById('formClienteTitle').innerHTML = '<i class="fa-solid fa-user-pen me-2"></i>Editar Cliente';
    document.getElementById('btnGuardarCliente').innerHTML = '<i class="fa-solid fa-arrows-rotate me-1"></i> Actualizar';
}

async function eliminarCliente(id) {
    if (!confirm('¿Está seguro de eliminar este cliente?')) return;

    try {
        const response = await fetch(`${API_URL}/cliente/eliminar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id_cliente: id })
        });
        const res = await response.json();

        if (res.error) {
            alert('Error: ' + res.error);
        } else {
            alert(res.mensaje);
            cargarClientes();
            cargarEmpresasSelect();
        }
    } catch (error) {
        console.error('Error al eliminar cliente:', error);
    }
}

function limpiarFormCliente() {
    document.getElementById('formCliente').reset();
    document.getElementById('cliente_id_edit').value = '';
    document.getElementById('formClienteTitle').innerHTML = '<i class="fa-solid fa-user-plus me-2"></i>Nuevo Cliente';
    document.getElementById('btnGuardarCliente').innerHTML = '<i class="fa-solid fa-floppy-disk me-1"></i> Guardar';
}

// ==================== SECCIÓN IMPUESTOS Y SIMULACIÓN ====================

async function cargarEmpresasSelect() {
    try {
        const response = await fetch(`${API_URL}/clientes/empresas`);
        const empresas = await response.json();
        const select = document.getElementById('selectEmpresa');
        select.innerHTML = '<option value="">Seleccione una empresa...</option>';
        empresas.forEach(e => {
            select.innerHTML += `<option value="${e.id_cliente}">${e.nombre} (${e.codigo})</option>`;
        });
    } catch (error) {
        console.error('Error al cargar empresas:', error);
    }
}

async function cargarProductosSelect() {
    try {
        const response = await fetch(`${API_URL}/productos`);
        const productos = await response.json();
        const select = document.getElementById('selectProducto');
        select.innerHTML = '<option value="">Seleccione actividad...</option>';
        productos.forEach(p => {
            select.innerHTML += `<option value="${p.codigo}">${p.nombre} (${p.codigo})</option>`;
        });
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

async function simularCalculo() {
    const prod = document.getElementById('selectProducto').value;
    const balance = document.getElementById('balance').value;

    if (!prod || !balance) {
        alert('Seleccione un producto e ingrese un balance para simular.');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/periodo/simular`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo_producto: prod, balance: parseFloat(balance) })
        });
        const res = await response.json();

        if (res.error) {
            alert(res.error);
        } else {
            document.getElementById('cardResultado').style.display = 'block';
            document.getElementById('resBase').textContent = `$${res.precio_base.toFixed(2)}`;
            document.getElementById('resExcedente').textContent = `$${res.excedente.toFixed(2)}`;
            document.getElementById('resBloques').textContent = res.bloques;
            document.getElementById('resAdicional').textContent = `$${res.adicional.toFixed(2)}`;
            document.getElementById('resTotal').textContent = `$${res.monto_impuesto.toFixed(2)}`;
            document.getElementById('resFormula').textContent = `Fórmula: ${res.formula}`;
        }
    } catch (error) {
        console.error('Error al simular cálculo:', error);
    }
}

async function guardarPeriodo(e) {
    e.preventDefault();

    const data = {
        id_cliente: parseInt(document.getElementById('selectEmpresa').value),
        codigo_producto: document.getElementById('selectProducto').value,
        fecha_desde: document.getElementById('fecha_desde').value,
        fecha_hasta: document.getElementById('fecha_hasta').value,
        balance: parseFloat(document.getElementById('balance').value)
    };

    try {
        const response = await fetch(`${API_URL}/periodo/guardar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const res = await response.json();

        if (res.error) {
            alert('Error: ' + res.error);
        } else {
            alert('Período impositivo guardado exitosamente');
            document.getElementById('formImpuesto').reset();
            document.getElementById('cardResultado').style.display = 'none';
            cargarHistorialPeriodos();
        }
    } catch (error) {
        console.error('Error al guardar período:', error);
    }
}

async function cargarHistorialPeriodos() {
    try {
        const response = await fetch(`${API_URL}/periodos`);
        const periodos = await response.json();
        const tbody = document.getElementById('tablaPeriodosBody');
        tbody.innerHTML = '';

        periodos.forEach(p => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="fw-bold">${p.nombre_cliente}</td>
                <td><span class="badge bg-outline-info border border-info text-info">${p.producto}</span></td>
                <td class="small">${p.fecha_desde} al ${p.fecha_hasta}</td>
                <td>$${parseFloat(p.balance).toFixed(2)}</td>
                <td class="small text-muted">${p.formula_aplicada}</td>
                <td class="text-end fw-bold text-success">$${parseFloat(p.monto_impuesto).toFixed(2)}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al cargar historial:', error);
    }
}