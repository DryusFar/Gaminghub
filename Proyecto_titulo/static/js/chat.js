document.addEventListener("DOMContentLoaded", function() {
   // Obtener el botón de emojis

    $(document).ready(function() {
        $("#textAreaExample3").emojioneArea({
          pickerPosition: "top"
        });
      });

    
	// Obtener la ventana modal de emojis
	/*var emojiModal = document.getElementById("emoji-modal");

	// Obtener el botón de cierre de la ventana modal de emojis
	var emojiModalClose = document.getElementById("emoji-modal-close");

	// Cuando se haga clic en el botón de emojis, mostrar la ventana modal
	emojiButton.onclick = function() {
		emojiModal.style.display = "block";
	}

	// Cuando se haga clic en el botón de cierre de la ventana modal de emojis, ocultar la ventana modal
	emojiModalClose.onclick = function() {
		emojiModal.style.display = "none";
	}

	// Cuando se haga clic en cualquier emoji, agregarlo al cuadro de entrada del chat
	var emojis = document.getElementsByClassName("emoji");
	for (var i = 0; i < emojis.length; i++) {
		emojis[i].onclick = function() {
			var inputBox = document.querySelector(".chat-form input[type='text']");
			inputBox.value += this.innerHTML;
		}
	}
    */


});

