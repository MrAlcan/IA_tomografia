document.addEventListener('DOMContentLoaded', () => {

    const nav_gestion = document.getElementById('nav_gestion_pacientes');
    const nav_consultas = document.getElementById('nav_consultas');
    nav_gestion.classList.add('active');
    nav_consultas.classList.add('active');
    const lista_gestion = document.querySelector('#nav_gestion_pacientes ul');
    console.log(lista_gestion);
    lista_gestion.classList.add('in');

    

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