function generarTabla(datos){
    const cuerpoTabla = document.querySelector('table tbody');
    //cuerpoTabla.innerHTML = '';

    var contador = 0;

    datos.forEach(dato => {
        console.log(dato);
        //console.log(dato.nombres);
        contador = contador + 1;
        const fila = document.createElement('tr');
        
        const numeroFila = document.createElement('td');
        numeroFila.textContent = contador;
        fila.appendChild(numeroFila);

        const nombresFila = document.createElement('td');
        nombresFila.textContent = dato.nombres;
        fila.appendChild(nombresFila);

        const apellidosFila = document.createElement('td');
        apellidosFila.textContent = dato.apellido_paterno + ' ' + dato.apellido_materno;
        fila.appendChild(apellidosFila);

        
        const cargoFila = document.createElement('td');
        cargoFila.textContent = dato.cargo;
        fila.appendChild(cargoFila);

        const rolFila = document.createElement('td');
        rolFila.textContent = dato.nombre_rol;
        fila.appendChild(rolFila);

        const accionesFila = document.createElement('td');
        const botonEditar = document.createElement('button');
        botonEditar.textContent = 'Editar';
        botonEditar.classList.add('btn');
        botonEditar.classList.add('btn-warning');
        botonEditar.classList.add('boton-editar');
        botonEditar.addEventListener('click', function() {
            localStorage.setItem('activoEdit', dato.id_usuario);
            window.location.href = `${url_base}/activo`;
        });
        accionesFila.appendChild(botonEditar);
        fila.appendChild(accionesFila);

        cuerpoTabla.appendChild(fila);
    });
}

document.addEventListener('DOMContentLoaded', () => {

    const datos_servidor = consultar_datos('/api/usuarios')
    .then(data=>{
        console.log(data);
        const usuarios = data.usuarios;
        console.log(usuarios);
        generarTabla(usuarios);
    })
    .catch(error=>{
        console.log(error);
    });
    //console.log(datos_servidor);
    //const usuarios = datos_servidor['usuarios'];
    

});