/*Boton salir grupo*/

$(document).ready(function() {
  $(".close").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar
    $("#myModal").modal("hide");
});
});

$(document).ready(function() {
  $(".close").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar
    $("#myModal2").modal("hide");
});
});

$(document).ready(function() {
  $(".btn-abrir-modal").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar
    $("#myModal").modal("show");
});
});

  $(document).ready(function() {
    $(".btn-abrir-modal").click(function() {
        var idGrupo = $(this).data("grupo-id");
        $("#grupo-id").text(idGrupo);
        var urlSalirGrupo = "/salir_grupo/" + idGrupo;
        $("#btn-salir").attr("href", urlSalirGrupo);
    });
});

/*boton eliminar grupo*/

$(document).ready(function() {
  $(".btn-abrir-modal2").click(function() {
    // Mostrar la modal correspondiente al botón de eliminar
    $("#myModal2").modal("show");
});
});

$(document).ready(function() {
  $(".btn-abrir-modal2").click(function() {
      var idGrupo = $(this).data("grupo-id");
      $("#grupo-id2").text(idGrupo);
      var urlEliminarGrupo = "/eliminar_grupo/" + idGrupo;
      $("#btn-eliminar").attr("href", urlEliminarGrupo);
  });
});