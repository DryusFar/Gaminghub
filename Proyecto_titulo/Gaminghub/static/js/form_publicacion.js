var titulo = document.getElementById("titulo");
var multimedia = document.getElementById("multimedia");
var contenido = document.getElementById("contenido");
const form = document.getElementById("form");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", e => {

    let mensajesMostrar = "";
    mensaje.innerHTML = "";

    entrar = false;

    if(titulo.value.length < 5 ||  titulo.value.length > 200){
        mensajesMostrar += 'El titulo debe tener un minimo de 5 caracteres y un maximo de 200 caracteres...<br>'
        entrar = true
    }

    if(contenido.value.length < 5 ||  contenido.value.length > 200){
        mensajesMostrar += 'El contenido debe tener un minimo de 5 caracteres y un maximo de 200 caracteres...<br>'
        entrar = true
    }

    if(multimedia.value == ""){
        mensajesMostrar += 'Debes ingresar una imagen, video o audio...<br>'
        entrar = true
    } else {
        const file = multimedia.files[0];
        const fileName = file.name;
        const validExtensions = ['jpg', 'jpeg', 'png', 'mp3', 'mp4'];

        const fileExtension = fileName.split('.').pop().toLowerCase();
        if (!validExtensions.includes(fileExtension)) {
            mensajesMostrar += 'Por favor, selecciona un archivo de audio, video o imagen válido...<br>';
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
