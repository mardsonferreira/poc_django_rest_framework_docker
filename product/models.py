from django.db import models

class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)

    def __str__(self):
        return '{} - {}'.format(self.name, self.price) 
