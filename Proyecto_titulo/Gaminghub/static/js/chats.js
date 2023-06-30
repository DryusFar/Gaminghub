var multimedia = document.getElementById("multimedia");
const form = document.getElementById("message-form");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", e => {

    let mensajesMostrar = "";
    mensaje.innerHTML = "";

    entrar = false;

    if(multimedia.value != null){
        const file = multimedia.files[0];
        const fileName = file.name;
        const validExtensions = ['jpg', 'jpeg', 'png'];

        const fileExtension = fileName.split('.').pop().toLowerCase();
        if (!validExtensions.includes(fileExtension)) {
            console.log("malalala")
            mensajesMostrar += 'Por favor, selecciona un archivo de imagen válido...<br>';
            entrar = true;
            multimedia.value = ''; // Limpiar el campo de entrada de archivo
        }  
    } 




    if(entrar){
        mensaje.innerHTML = mensajesMostrar;
        e.preventDefault();
    }else{
        mensaje.innerHTML = "";
    }

});
