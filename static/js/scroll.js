$(document).ready(function() {
    // Manejar clic en el botón "Add to Cart"
    $(".add-to-cart-btn").click(function() {
        var form = $(this).closest("form");
        var product = form.find("input[name='product']").val();
        
        $.ajax({
            url: form.attr("action"),
            type: "POST",
            data: form.serialize(),
            success: function(data) {
                var cartQuantity = data.cart_quantity;
                form.siblings(".text-center").text(cartQuantity + " in Cart");
                form.siblings(".row1").show();
                form.hide();
                location.reload();  // Recargar la página para reflejar los cambios
            },
            error: function() {
                alert("Error occurred");
            }
        });
        
        return false;  // Evitar que se recargue la página
    });

    // Manejar clic en el botón "Remove from Cart"
    $(".remove-from-cart-btn").click(function() {
        var form = $(this).closest("form");
        var product = form.find("input[name='product']").val();
        
        $.ajax({
            url: form.attr("action"),
            type: "POST",
            data: form.serialize(),
            success: function(data) {
                var cartQuantity = data.cart_quantity;
                form.siblings(".text-center").text(cartQuantity + " in Cart");
                if (cartQuantity <= 0) {
                    form.siblings(".add-to-cart-form").show();
                }
            },
            error: function() {
                alert("Error occurred");
            }
        });
        
        return false;  // Evitar que se recargue la página
    });
});
