# from django.db import models
# from django.core.validators import MinValueValidator
# from django.utils.translation import gettext_lazy as _
# from django.conf import settings
# from django.contrib.auth import get_user_model
# User = get_user_model() # Import from your accounts app
# from django.conf import settings
# from django.utils import timezone
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from accounts.models import Customer


# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     current_price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField(default=0)
#     primary_image = models.ImageField(upload_to='products/')

#     def __str__(self):
#         return self.name

#     def is_in_stock(self):
#         """Returns True if the product is in stock."""
#         return self.stock > 0

#     def reduce_stock(self, quantity=1):
#         """Reduces the stock by the specified quantity."""
#         if self.stock >= quantity:
#             self.stock -= quantity
#             self.save()
#             return True
#         return False
# class ProductImage(models.Model):
#     """High-quality product imagery"""
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='images'
#     )
#     image = models.ImageField(
#         _('Image'),
#         upload_to='products/%Y/%m/'
#     )
#     alt_text = models.CharField(
#         _('Alt Text'),
#         max_length=100,
#         blank=True,
#         help_text=_('Accessibility description')
#     )
#     is_primary = models.BooleanField(
#         _('Primary Image'),
#         default=False
#     )
#     order = models.PositiveIntegerField(
#         _('Display Order'),
#         default=0
#     )

#     class Meta:
#         verbose_name = _('Product Image')
#         verbose_name_plural = _('Product Images')
#         ordering = ['order']

#     def __str__(self):
#         return f"Image for {self.product.sku}"

# class Inventory(models.Model):
#     """Luxury inventory tracking"""
#     product = models.OneToOneField(
#         Product,
#         on_delete=models.CASCADE,
#         primary_key=True,
#         related_name='inventory'
#     )
#     stock = models.PositiveIntegerField(
#         _('Available Stock'),
#         default=0
#     )
#     reserved = models.PositiveIntegerField(
#         _('Reserved Stock'),
#         default=0
#     )
#     last_restock = models.DateField(
#         _('Last Restock'),
#         null=True,
#         blank=True
#     )

#     class Meta:
#         verbose_name = _('Inventory')
#         verbose_name_plural = _('Inventories')

#     @property
#     def available(self):
#         return self.stock - self.reserved

#     def __str__(self):
#         return f"Inventory for {self.product.sku}"

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     @property
#     def total(self):
#         return sum(item.subtotal for item in self.items.all())

#     @property
#     def item_count(self):
#         return self.items.count()

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price_at_add = models.DecimalField(max_digits=10, decimal_places=2)

#     @property
#     def subtotal(self):
#         return self.price_at_add * self.quantity

#     class Meta:
#         unique_together = ['cart', 'product']  # Prevents duplicate items

# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_paid = models.BooleanField(default=False)
#     order_date = models.DateField(default=timezone.now)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"
    
# # class Customer(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     phone = models.CharField(max_length=20, blank=True)
# #     address = models.TextField(blank=True)

# #     def __str__(self):
# #         return self.user.username
# # from .models import Customer  # your Customer model

# # @receiver(post_save, sender=User)
# # def create_customer(sender, instance, created, **kwargs):
# #     if created:
# #         Customer.objects.create(user=instance)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

# Use your custom user model
User = settings.AUTH_USER_MODEL

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    primary_image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            self.save()
            return True
        return False


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to='products/%Y/%m/')
    alt_text = models.CharField(_('Alt Text'), max_length=100, blank=True, help_text=_('Accessibility description'))
    is_primary = models.BooleanField(_('Primary Image'), default=False)
    order = models.PositiveIntegerField(_('Display Order'), default=0)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True, related_name='inventory')
    stock = models.PositiveIntegerField(_('Available Stock'), default=0)
    reserved = models.PositiveIntegerField(_('Reserved Stock'), default=0)
    last_restock = models.DateField(_('Last Restock'), null=True, blank=True)

    class Meta:
        verbose_name = _('Inventory')
        verbose_name_plural = _('Inventories')

    @property
    def available(self):
        return self.stock - self.reserved

    def __str__(self):
        return f"Inventory for {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def item_count(self):
        return self.items.count()


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price_at_add = models.DecimalField(max_digits=10, decimal_places=2)

#     @property
#     def subtotal(self):
#         return self.price_at_add * self.quantity

#     class Meta:
#         unique_together = ['cart', 'product']
# class CartItem(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, 
#                             related_name='cart_items',
#                             on_delete=models.CASCADE)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'product']

#     @property
#     def subtotal(self):
#         return self.product.price * self.quantity

# class CartItem(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='cart_items'
#     )
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'product']
# In shop/models.py - ensure this matches your actual model:
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items', default=None)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_add = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product']


# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_paid = models.BooleanField(default=False)
#     order_date = models.DateField(default=timezone.now)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    shipping_address = models.TextField(default="Not Provided")
    payment_status = models.CharField(max_length=20, default='Pending')
    order_status = models.CharField(max_length=20, default='Processing')

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.quantity * self.price
from django.db import models
from django.conf import settings
from .models import Order  # or wherever your Order model is

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
