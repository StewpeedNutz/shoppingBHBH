from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=20, default='')


    def register(self):
        self.save()



    def isExist(self):
        if Customer.objects.filter(phone=self.phone).exists() or Customer.objects.filter(email=self.email).exists() or Customer.objects.filter(username=self.username).exists():
            return True
        else:
            return False



