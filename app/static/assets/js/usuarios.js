document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_usuarios');
    const nav_usuarios = document.getElementById('nav_usuarios');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_usuarios ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    const botonAgregar = document.getElementById('boton_agregar_usuario');
    botonAgregar.addEventListener('click', function() {
        window.location.href = `/usuarios/agregar`;
    });




    
    /*const label_inicio = document.querySelector('.dataTables_length label');
    console.log(label_inicio);
    label_inicio.innerHTML = label_inicio.innerHTML.replace(/Show/, 'Mostrar');
    label_inicio.innerHTML = label_inicio.innerHTML.replace(/entries/, 'entradas');*/

    /*const label_buscar = document.querySelector('.dataTables_filter label');
    console.log(label_buscar);
    //label_buscar.innerHTML = label_buscar.innerHTML.replace(/Search:/, `Search:`);
    label_buscar.setAttribute('style','color: white;');

    const label_pie_tabla = document.getElementById('dataTable_info');
    label_pie_tabla.innerHTML = label_pie_tabla.innerHTML.replace(/Showing/, 'Mostrando');
    label_pie_tabla.innerHTML = label_pie_tabla.innerHTML.replace(/to/, 'a');
    label_pie_tabla.innerHTML = label_pie_tabla.innerHTML.replace(/of/, 'de');
    label_pie_tabla.innerHTML = label_pie_tabla.innerHTML.replace(/entries/, 'entradas');*/
});