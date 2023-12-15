from django.forms.models import model_to_dict

from apps.categories.dao import CategoryDAO


class CategoryService:
    def __init__(self, category_dao: CategoryDAO):
        self._category_dao = category_dao

    def execute(self) -> list[dict]:
        categories = self._category_dao.get_parent_categories()
        return [self._get_tree(category) for category in categories]

    def _get_tree(self, category) -> dict:
        tree = model_to_dict(category, fields=["name", "id"])
        if category.children_category.all().exists():
            children = list()
            for child in category.children_category.all():
                children.append(self._get_tree(child))
            tree["children_category"] = children
        return tree


category_service = CategoryService(CategoryDAO())
