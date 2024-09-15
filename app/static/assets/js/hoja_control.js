document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_pacientes');
    const nav_pacientes = document.getElementById('nav_signos_vitales');
    nav_gestion.classList.add('active');
    nav_pacientes.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_pacientes ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    const botonAgregar = document.getElementById('boton_agregar_hoja');
    botonAgregar.addEventListener('click', function() {
        window.location.href = `/control_signos_vitales/agregar`;
    });

});