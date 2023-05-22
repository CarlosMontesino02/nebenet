from nebenet_app.models import Order

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si el carrito ya está almacenado en la sesión
        if 'cart' not in request.session:
            # Verificar si hay un carrito almacenado en el modelo Order
            if request.user.is_authenticated:
                try:
                    cart = Order.objects.get(customer=request.user, status=False)
                    request.session['cart'] = {
                        'product_id': cart.product_id,
                        'quantity': cart.quantity
                    }
                except Order.DoesNotExist:
                    # No hay carrito en el modelo Order, inicializar uno vacío en la sesión
                    request.session['cart'] = {}

        response = self.get_response(request)

        return response