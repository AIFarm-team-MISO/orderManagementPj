from django.db import models

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    Product_code = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.order_number
