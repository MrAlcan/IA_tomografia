document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_resultados_tomografias');
    const nav_usuarios = document.getElementById('nav_gestion_consultas');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_consultas ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    const botonAgregar = document.getElementById('boton_agregar_usuario');
    botonAgregar.addEventListener('click', function() {
        window.location.href = `/usuarios/agregar`;
    });

});

const canvas = document.getElementById('canvasImagenes');
const ctx = canvas.getContext('2d');
const entradaImagenes = document.getElementById('entradaImagenes');
const contenedorMiniaturas = document.getElementById('contenedorMiniaturas');

let imagenesCargadas = []; 

entradaImagenes.addEventListener('change', function(event) {
    const archivos = event.target.files;

    Array.from(archivos).forEach(archivo => {
        const lector = new FileReader();
        lector.onload = function(e) {
            const img = new Image();
            img.src = e.target.result;
            img.onload = function() {
                imagenesCargadas.push(img.src); 
                const contenedorMiniatura = document.createElement('div');
                contenedorMiniatura.classList.add('contenedor-miniatura');
                const miniatura = document.createElement('img');
                miniatura.src = e.target.result;
                miniatura.classList.add('miniatura');
                const botonEliminar = document.createElement('div');
                botonEliminar.classList.add('boton-eliminar');
                botonEliminar.innerText = 'X';
                botonEliminar.onclick = function() {
                    contenedorMiniatura.remove(); 
                    imagenesCargadas = imagenesCargadas.filter(src => src !== img.src); 
                    ctx.clearRect(0, 0, canvas.width, canvas.height); 
                };

                contenedorMiniatura.appendChild(miniatura);
                contenedorMiniatura.appendChild(botonEliminar);
                contenedorMiniaturas.appendChild(contenedorMiniatura);
                if (imagenesCargadas.length === 1) {
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                }
            };
        };
        lector.readAsDataURL(archivo);
    });
});

contenedorMiniaturas.addEventListener('click', function(event) {
    if (event.target.tagName === 'IMG') {
        const src = event.target.src;
        const img = new Image();
        img.src = src;
        img.onload = function() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        };
    }
});
document.getElementById('limpiarCampos').addEventListener('click', function() {
    document.getElementById('formularioImagenes').reset();
    const canvas = document.getElementById('canvasImagenes');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const contenedorMiniaturas = document.getElementById('contenedorMiniaturas');
    contenedorMiniaturas.innerHTML = '';
});

document.getElementById('codigoPaciente').addEventListener('change', function() {
    const pacienteId = this.value;

    if (pacienteId) {
        fetch(`/obtener_nombre_paciente/${pacienteId}`)
            .then(response => response.json())
            .then(data => {
                if (data.nombres && data.apellido_paterno && data.apellido_materno) {
                    const nombreCompleto = data.nombres + ' ' + data.apellido_paterno + ' ' + data.apellido_materno;
                    document.getElementById('nombrePaciente').value = nombreCompleto;
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('nombrePaciente').value = '';
    }
});