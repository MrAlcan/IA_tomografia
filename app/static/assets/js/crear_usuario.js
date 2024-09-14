/*function generarSelect(datos){

    const selectRoles = document.getElementById('input_rol');

    datos.forEach(dato => {
        console.log(dato);
        const opcionRol = document.createElement('option');
        opcionRol.innerText = dato.nombre;
        const id_rol = ''+dato.id_rol+'';
        opcionRol.setAttribute('value', id_rol);
        selectRoles.appendChild(opcionRol);
    });

}*/

document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_usuarios');
    const nav_usuarios = document.getElementById('nav_usuarios');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_usuarios ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    console.log(document.cookie.split("=")[1]);

    /*const nav_gestion = document.getElementById('nav_gestion_usuarios');
    const nav_usuarios = document.getElementById('nav_usuarios');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_usuarios ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');



    const datos_servidor = consultar_datos('/api/usuarios/agregar')
    .then(data=>{
        console.log(data);
        const roles = data.roles;
        console.log(roles);
        generarSelect(roles);
    })
    .catch(error=>{
        console.log(error);
    });
    //console.log(datos_servidor);
    //const usuarios = datos_servidor['usuarios'];*/
    
    

});
/*
document.getElementById('crear_usuario_form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevenir el envío del formulario de forma tradicional


    const nombres = document.getElementById('input_nombres').value;
    const ap_pat = document.getElementById('input_apellido_paterno').value;
    const ap_mat = document.getElementById('input_apellido_materno').value;
    const carnet = document.getElementById('input_carnet').value;
    const cargo = document.getElementById('input_cargo').value;
    const nombre_cuenta = document.getElementById('input_nombre_cuenta').value;
    const contrasena = document.getElementById('input_contrasena').value;
    const rol = document.getElementById('input_rol').value;

    //const datos = Object.fromEntries(datos_formulario);
    const datos = {
        nombre_cuenta: nombre_cuenta,
        contrasena: contrasena,
        nombres: nombres,
        ap_paterno: ap_pat,
        ap_materno: ap_mat,
        carnet: carnet,
        cargo: cargo,
        id_rol: rol
    };
    console.log(datos);

    const nuevo_usuario = consultar_datos('/api/usuarios/agregar', 'POST', datos)
    .then(data=>{
        console.log(data);
        if(data.codigo==200){
            console.log("usuario creado correctamente");
            console.log(data.nuevo_usuario);
            //window.location.href = '/usuarios';
        }else if(data.codigo==400){
            console.log("usuario no creado");
        }
    })
    .catch(error=>{
        console.log(error);
    });

    
});*/