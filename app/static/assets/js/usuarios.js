function generarTabla(datos){
    const botonAgregar = document.getElementById('boton_agregar_usuario');
    botonAgregar.addEventListener('click', function() {
        window.location.href = `${url_base}/usuarios/agregar`;
    });


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
        /*
        <ul class="d-flex justify-content-center">
            <li class="mr-3"><a href="#" class="text-secondary"><i class="fa fa-edit"></i></a></li>
            <li><a href="#" class="text-danger"><i class="ti-trash"></i></a></li>
        </ul>*/

        const accionesFila = document.createElement('td');
        const listaAcciones = document.createElement('ul');
        listaAcciones.classList.add('d-flex');
        listaAcciones.classList.add('justify-content-center');
        
        const listaEditar = document.createElement('li');
        listaEditar.classList.add('mr-3');
        const listaEliminar = document.createElement('li');
        const botonEditar = document.createElement('a');
        botonEditar.setAttribute('href', `/usuarios/editar/${dato.id_usuario}`);
        botonEditar.classList.add('text-secondary');
        const botonEliminar = document.createElement('a');
        botonEliminar.setAttribute('href', '#');
        botonEliminar.classList.add('text-danger');
        const iconoEditar = document.createElement('i');
        iconoEditar.classList.add('fa');
        iconoEditar.classList.add('fa-edit');
        const iconoEliminar = document.createElement('i');
        iconoEliminar.classList.add('ti-trash')
        
        botonEditar.appendChild(iconoEditar);
        botonEliminar.appendChild(iconoEliminar);
        listaEditar.appendChild(botonEditar);
        listaEliminar.appendChild(botonEliminar);
        listaAcciones.appendChild(listaEditar);
        listaAcciones.appendChild(listaEliminar);
        accionesFila.appendChild(listaAcciones);
        
        

        

        /*const accionesFila = document.createElement('td');
        const botonEditar = document.createElement('button');*/
        /*botonEditar.textContent = 'Editar';
        botonEditar.classList.add('btn');
        botonEditar.classList.add('btn-warning');
        botonEditar.classList.add('boton-editar');
        botonEditar.addEventListener('click', function() {
            localStorage.setItem('activoEdit', dato.id_usuario);
            window.location.href = `${url_base}/activo`;
        });
        accionesFila.appendChild(botonEditar);*/
        fila.appendChild(accionesFila);

        cuerpoTabla.appendChild(fila);
    });
}

document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_usuarios');
    const nav_usuarios = document.getElementById('nav_usuarios');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_usuarios ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

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