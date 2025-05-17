# from django.views.generic import TemplateView
# from django.contrib.admin.views.decorators import staff_member_required
# from django.utils.decorators import method_decorator
# from django.db.models import Count, Sum
# from shoe_shop.models import Product, Order # type: ignore

# @method_decorator(staff_member_required, name='dispatch')
# class ProductCurationDashboard(TemplateView):
#     template_name = 'admin/product_curation.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Collection performance
#         context['collection_stats'] = (
#             Product.objects.values('collection')
#             .annotate(
#                 total_products=Count('id'),
#                 total_sold=Sum('order_items__quantity')
#             )
#         )
        
#         # Low inventory alerts
#         context['low_stock'] = (
#             Product.objects.filter(inventory__available__lt=5)
#             .select_related('inventory')
#             .order_by('inventory__available')
#         )
        
#         return context