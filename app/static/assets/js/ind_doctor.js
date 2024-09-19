document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_consultas');
    const nav_usuarios = document.getElementById('nav_indicaciones_doctor');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_consultas ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

 

});