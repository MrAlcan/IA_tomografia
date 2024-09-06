const url_base = '';
const token = localStorage.getItem('token');

const consultar_datos = async (direccion, metodo='GET', cuerpo=null) => {
    console.log('datos token');
    console.log(token)
    try {
        const respuesta = await fetch(`${url_base}${direccion}`, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: cuerpo ? JSON.stringify(cuerpo) : null
        });

        if (!respuesta.ok) {
            console.log(respuesta);
            if(respuesta.status==422 || respuesta.status==401){
                console.log("sin autorizacion");
                window.location.href = '/ingresar';
            }
            throw new Error('Error en la respuesta del servidor');
        }
        const resultado = await respuesta.json();
        console.log('Éxito:', resultado);
        if(resultado.codigo==200){
            //localStorage.setItem('token', resultado.token);
            //console.log(resultado.token)
            console.log('normal')
            console.log(resultado)
            return await resultado;
        }
        if(resultado.codigo!=200){
            console.log('Error por alguna razon')
        }
        //return resultado;
    } catch (error) {
        console.error('Errores:', error);
    }
}