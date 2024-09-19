document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_lista_tomografias');
    const nav_usuarios = document.getElementById('nav_gestion_consultas');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_consultas ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    const botonAgregar = document.getElementById('boton_agregar_estudio');
    botonAgregar.addEventListener('click', function() {
        window.location.href = `/tomografia_resultados`;
    });

});