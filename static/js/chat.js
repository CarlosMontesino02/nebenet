$(document).ready(function() {
    $("#comment-form").on("submit", function(event) {
      event.preventDefault();
      var formData = $(this).serialize();
      var form = $(this);
  
      $.ajax({
        url: form.attr("action"),
        type: "POST",
        data: formData,
        success: function(response) {
          updateComments(response);
          form.trigger("reset"); // Restablecer el formulario después de enviarlo
          form.show(); // Mostrar el formulario después de enviarlo
        },
        error: function() {
          alert("Error occurred");
        }
      });
    });
  
    function updateComments(comments) {
      var commentContainer = $(".comentarios");
      var commentsHTML = "";
  
      for (var i = 0; i < comments.length; i++) {
        var comment = comments[i];
        var commentHTML =
          '<p>' +
          '<span class="fechaco">' + comment.ti_time + '</span>' +
          '<span class="nomuser">' + comment.co_user + '</span>' +
          '<span class="cosabla">:</span>' +
          '<span class="cotexto">' + comment.co_text + '</span>' +
          '</p>';
        commentsHTML += commentHTML; // Utilizar el operador += para agregar los comentarios en orden ascendente
      }
  
      commentContainer.html(commentsHTML);
    }
  });