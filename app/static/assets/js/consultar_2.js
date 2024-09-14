// Función para manejar la navegación
async function navegar(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')  // Envía el token en la cabecera
            }
        });

        if (response.status === 200) {
            // Si el token es válido, renderiza la vista
            console.log('ingreso');
            //console.log(await response);
            //console.log(await response.text());
            //console.log(await response.json());
            
            document.body.innerHTML = await response.text();
        } else if (response.status === 401) {
            // Si el token es inválido o ha expirado, redirige al login
            window.location.href = '/ingresar';
        }
    } catch (error) {
        console.error('Error al navegar:', error);
    }
}

// Ejemplo de uso: Navegar a la vista de usuarios
document.getElementById('usuarios-link').addEventListener('click', function(event) {
    event.preventDefault();  // Prevenir la recarga de la página
    navegar('/usuarios');
});

// Ejemplo de uso: Navegar a la vista de roles
document.getElementById('roles-link').addEventListener('click', function(event) {
    event.preventDefault();
    navegar('/roles');
});
