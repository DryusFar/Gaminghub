$(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
      // Mostrar la modal correspondiente al botón de eliminar comentario
      $("#myModal2").modal("show");
});
$(".close").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar comentario
    $("#myModal2").modal("hide");
});
});

$(document).ready(function() {
    $(".btn-abrir-modal2").click(function() {
        var idComentario = $(this).data("id-comentario");
        $("#comentario-id").text(idComentario);
        var urlEliminarComentario = "/eliminar_comentario/" + idComentario;
        $("#btn-eliminar").attr("href", urlEliminarComentario);
    });
});