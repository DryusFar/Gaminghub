$(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
      // Mostrar la modal correspondiente al botón de eliminar
      $("#myModal2").modal("show");
});
});
  
$(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
        var idPublicacion = $(this).data("id-publicacion");
        $("#publicacion-id").text(idPublicacion);
        var urlEliminarPublicacion = "/eliminar_publicacion/" + idPublicacion;
        $("#btn-eliminar").attr("href", urlEliminarPublicacion);
    });
});