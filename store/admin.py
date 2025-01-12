from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart

class AdminProduct(admin.ModelAdmin):
    list_display =['id','name','price','category','description']

class AdminCustomer(admin.ModelAdmin):
    list_display =['id','name','username','email','phone','password']

class AdminCart(admin.ModelAdmin):
    list_display =['id','username','product','image','quantity','price']



admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Customer, AdminCustomer)
admin.site.register(Cart, AdminCart)