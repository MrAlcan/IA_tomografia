function generarSelect(datos){

    const selectRoles = document.getElementById('input_rol');

    datos.forEach(dato => {
        console.log(dato);
        const opcionRol = document.createElement('option');
        opcionRol.innerText = dato.nombre;
        const id_rol = ''+dato.id_rol+'';
        opcionRol.setAttribute('value', id_rol);
        selectRoles.appendChild(opcionRol);
    });

}

let id_usuario_edit = '';

function llenar_datos_usuario(dato){
    id_usuario_edit = dato.id_usuario;
    console.log(id_usuario_edit);
    const input_nombres = document.getElementById('input_nombres');
    const input_apellido_paterno = document.getElementById('input_apellido_paterno');
    const input_apellido_materno = document.getElementById('input_apellido_materno');
    const input_cargo = document.getElementById('input_cargo');
    const input_carnet = document.getElementById('input_carnet');
    const input_nombre_cuenta = document.getElementById('input_nombre_cuenta');
    const input_rol = document.getElementById('input_rol');
    
    input_nombres.value = dato.nombres;
    input_apellido_paterno.value = dato.apellido_paterno;
    input_apellido_materno.value = dato.apellido_materno;
    input_cargo.value = dato.cargo;
    input_carnet.value = dato.carnet;
    input_nombre_cuenta.value = dato.cuenta;
    input_rol.value = dato.id_rol;

    
    
}

document.addEventListener('DOMContentLoaded', () => {
    const nav_gestion = document.getElementById('nav_gestion_usuarios');
    const nav_usuarios = document.getElementById('nav_usuarios');
    nav_gestion.classList.add('active');
    nav_usuarios.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_usuarios ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    const id_usuario_editar = document.getElementById('id_usuario_editar').textContent;

    console.log(id_usuario_editar);
    const datos_servidor = consultar_datos(`/api/usuarios/editar/${id_usuario_editar}`)
    .then(data=>{
        console.log(data);
        const roles = data.roles;
        console.log(roles);
        generarSelect(roles);
        const usuario_editar = data.usuario_editar;
        llenar_datos_usuario(usuario_editar);

    })
    .catch(error=>{
        console.log(error);
    });
    //console.log(datos_servidor);
    //const usuarios = datos_servidor['usuarios'];
    
    

});

document.getElementById('crear_usuario_form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevenir el envío del formulario de forma tradicional


    const nombres = document.getElementById('input_nombres').value;
    const ap_pat = document.getElementById('input_apellido_paterno').value;
    const ap_mat = document.getElementById('input_apellido_materno').value;
    const carnet = document.getElementById('input_carnet').value;
    const cargo = document.getElementById('input_cargo').value;
    const nombre_cuenta = document.getElementById('input_nombre_cuenta').value;
    const rol = document.getElementById('input_rol').value;

    //const datos = Object.fromEntries(datos_formulario);
    const datos = {
        nombre_cuenta: nombre_cuenta,
        nombres: nombres,
        contrasena: null,
        ap_paterno: ap_pat,
        ap_materno: ap_mat,
        carnet: carnet,
        cargo: cargo,
        id_rol: rol
    };

    const nuevo_usuario = consultar_datos(`/api/usuarios/editar/${id_usuario_edit}`, 'POST', datos)
    .then(data=>{
        console.log(data);
        if(data.codigo==200){
            console.log("usuario modificado correctamente");
            console.log(data.nuevo_usuario);
            window.location.href = '/usuarios';
        }else if(data.codigo==400){
            console.log("usuario no modificado");
        }
    })
    .catch(error=>{
        console.log(error);
    });

    
});