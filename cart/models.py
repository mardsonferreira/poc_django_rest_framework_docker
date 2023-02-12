from django.db import models

from product.models import Products

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    total = models.FloatField(null=False)
    products = models.ManyToManyField(Products)

    def __str__(self):
        return '{}'.format(self.total)