from django.db import models

class Product(models.Model):
    name = models.TextField()
    times_used = models.IntegerField(default=0)

class Recipe(models.Model):
    name = models.TextField()
    products = models.ManyToManyField('Product', through='RecipeProduct')

class RecipeProduct(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    weight = models.IntegerField()

    class Meta:
        unique_together = ('recipe', 'product')
