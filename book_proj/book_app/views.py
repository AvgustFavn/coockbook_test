from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, Recipe, RecipeProduct


def add_product_to_recipe(request, recipe_id, product_id, weight):
    """add_product_to_recipe с параметрами recipe_id, product_id, weight. Функция добавляет к указанному рецепту
    указанный продукт с указанным весом. Если в рецепте уже есть такой продукт, то функция должна поменять его вес
    в этом рецепте на указанный."""
    try:
        recipe = get_object_or_404(RecipeProduct, recipe_id=recipe_id, product_id=product_id)
    except Http404:
        recipe = None

    if recipe:
        recipe.weight = weight
        recipe.save()
        return HttpResponse('Граммовка изменена!')
    else:
        recipe = Recipe.objects.filter(id=recipe_id).first()
        if recipe:
            prod = Product.objects.filter(id=product_id).first()
            new_prod = RecipeProduct.objects.create(recipe=recipe, product=prod, weight=weight)
            return HttpResponse('продукт в рецепт добавлен!')
        else:
            return HttpResponse(status=404)





def cook_recipe(request, recipe_id):
    """cook_recipe c параметром recipe_id. Функция увеличивает на единицу количество приготовленных блюд для каждого
    продукта, входящего в указанный рецепт."""
    recipe = get_object_or_404(Recipe, id=recipe_id)

    for recipe_product in recipe.recipeproduct_set.all():
        product = recipe_product.product

        product.times_used += 1
        product.save()

    return HttpResponse("Кол-во приготовленных продуктов увеличилось!")

def show_recipes_without_product(request, product_id):
    """show_recipes_without_product с параметром product_id. Функция возвращает HTML страницу, на которой размещена
    таблица. В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует, или
    присутствует в количестве меньше 10 грамм. Страница должна генерироваться с использованием Django templates.
    Качество HTML верстки не оценивается."""
    product = Product.objects.get(id=product_id)
    recipes = []
    recipes.extend(RecipeProduct.objects.exclude(Q(weight__gte=10)).all())
    all_recipes = Recipe.objects.all()
    recipes_set = set()

    for recipe in all_recipes:
        if RecipeProduct.objects.filter(product_id=product_id, recipe_id=recipe.id).exists():
            rp = RecipeProduct.objects.filter(product_id=product_id, recipe_id=recipe.id).first()
            if rp.weight < 10:
                recipes_set.add(recipe)
        else:
            recipes_set.add(recipe)

    print(recipes_set)
    return render(request, 'table.html', context={'recipes': recipes_set})
