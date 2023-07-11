/*var password1 = document.getElementById("password1");
var password2 = document.getElementById("password2");
const form = document.getElementById("form");
var mensaje = document.getElementById("warnings");

form.addEventListener("submit", e => {

    let mensajesMostrar = "";
    mensaje.innerHTML = "";

    entrar = false;

    if(password1.value.length < 8){
        mensajesMostrar += 'La contraseña debe tener minimo 8 caracteres...<br>'
        entrar = true
    }

    if(!/[A-Z]/.test(password1.value)){  
        mensajesMostrar += 'La contraseña debe tener minimo 1 mayuscula...<br>';
        entrar = true;
    }

    if(password1.value != password2.value){
        mensajesMostrar += 'Las contraseñas no coinciden...';
        entrar = true; 

    }

    if(entrar){
        mensaje.innerHTML = mensajesMostrar;
        e.preventDefault();
    }else{
        mensaje.innerHTML = "";
    }

});
*/
