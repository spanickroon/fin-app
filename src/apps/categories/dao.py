from apps.categories.models import Category


class CategoryDAO:
    def get_parent_categories(self):
        return Category.objects.filter(parent_category__isnull=True)
