# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import mail_admins
# from .models import Inventory

# @receiver(post_save, sender=Inventory)
# def check_inventory_levels(sender, instance, **kwargs):
#     if instance.available < 5:  # Threshold for luxury items
#         mail_admins(
#             subject=f"Low Stock Alert: {instance.product.name}",
#             message=f"Only {instance.available} units left of {instance.product.sku}",
#             fail_silently=True
#         )