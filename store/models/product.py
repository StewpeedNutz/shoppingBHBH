from django.db import models
from .category import Category



class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=200,default='', blank=True,null=True)
    image = models.ImageField(upload_to='upload/products/')


    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_product_by_category_id(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()






    def __str__(self):
        return self.name