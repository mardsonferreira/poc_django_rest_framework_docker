# Generated by Django 3.2.16 on 2023-02-11 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_alter_products_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('products', models.ManyToManyField(to='product.Products')),
            ],
        ),
    ]
