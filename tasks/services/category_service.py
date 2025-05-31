import random
from tasks.models import Category
from tasks.services.interfaces import ICategoryService


class CategoryService(ICategoryService):

    def assign_random_color_to_category(self):
        used_colors = Category.objects.values_list('color', flat=True)
        colors = ['#E53935', '#8E24AA', '#3949AB', '#039BE5', '#00897B', '#43A047', '#FDD835', '#FB8C00', '#D81B60']
        available_colors = list(set(colors) - set(used_colors))

        if not available_colors:
            return random.choice(colors)
        return random.choice(available_colors)

    def get_all_categories(self):
        return Category.objects.all().order_by('name')