var correo = document.getElementById("correo")
var nombre = document.getElementById("nombre");
var apellido = document.getElementById("apellido");
var genero = document.getElementById("genero");
var fecha_nac = document.getElementById("fecha_nac");
var edad = document.getElementById("edad");
var avatar = document.getElementById("myImage");
var descripcion = document.getElementById("descripcion");
const form = document.getElementById("form");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", e => {

    let mensajesMostrar = "";
    mensaje.innerHTML = "";

    let regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,4})+$/

    entrar = false;

    if (!regexEmail.test(correo.value)) {
        mensajesMostrar += 'El email no es valido <br>'
        entrar = true
    }

    if(nombre.value.length > 50){
        mensajesMostrar += 'Largo de nombre invalido...(50)<br>'
        entrar = true
    }

    if(apellido.value.length > 50){
        mensajesMostrar += 'Largo de apellido invalido...(50)<br>'
        entrar = true
    }

    if(fecha_nac.value > "2019/12/12"){
        mensajesMostrar += 'Fecha de nacimiento invalida...<br>'
        entrar = true
    }

    if(edad.value > 150){
        mensajesMostrar += 'La edad debe ser valida...(entre 0 y 150)<br>'
        entrar = true
    }

    if(edad.value < 0){
        mensajesMostrar += 'La edad debe ser valida...(entre 0 y 150)<br>'
        entrar = true
    }

    if(genero.value.length > 50){
        mensajesMostrar += 'Largo de genero invalido...(50)<br>'
        entrar = true
    }

    if(descripcion.value.length > 300){
        mensajesMostrar += 'La descripcion no cumple con el limite de caracteres...(300)<br>'
        entrar = true
    }

    if(entrar){
        mensaje.innerHTML = mensajesMostrar;
        e.preventDefault();
    }else{
        mensaje.innerHTML = "";
    }

});

function showSelectedImage(event) {
    var input = event.target;
    var img = document.getElementById('selectedImage');

    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function(e) {
        img.src = e.target.result;
      };

      reader.readAsDataURL(input.files[0]);
    }
  }

