from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

from shop.models import CartItem, Product

@login_required
@require_POST
def ajax_cart_update(request):
    try:
        data = json.loads(request.body)
        product_id = data['product_id']
        action = data['action']
        
        product = Product.objects.get(pk=product_id)
        cart, _ = cart.objects.get_or_create(user=request.user, is_active=True)
        
        if action == 'add':
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'price_at_add': product.current_price}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
                
        elif action == 'remove':
            CartItem.objects.filter(cart=cart, product=product).delete()
            
        return JsonResponse({
            'success': True,
            'cart_total': cart.total,
            'item_count': cart.items.count()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)