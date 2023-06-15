
$(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
      // Mostrar la modal correspondiente al botón de eliminar
      $("#myModal2").modal("show");
  });

  $(".close").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar
    $("#myModal2").modal("hide");
});
  });
  
  $(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
        var idSala = $(this).data("sala-id");
        var urlEliminarSala = "/eliminar_sala/" + idSala;
        $("#btn-eliminar").attr("href", urlEliminarSala);
    });
  });