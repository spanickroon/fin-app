from django.test import TestCase

from apps.categories.dao import CategoryDAO
from apps.categories.models import Category


class CategoryDAOTestCase(TestCase):

    def setUp(self):
        self.category_dao = CategoryDAO()

    def test_get_parent_categories(self):
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        subcategory1 = Category.objects.create(name='Subcategory 1', parent_category=category1)
        subcategory2 = Category.objects.create(name='Subcategory 2', parent_category=category1)

        parent_categories = self.category_dao.get_parent_categories()

        self.assertEqual(parent_categories.count(), 2)
        self.assertIn(category1, parent_categories)
        self.assertIn(category2, parent_categories)
        self.assertNotIn(subcategory1, parent_categories)
        self.assertNotIn(subcategory2, parent_categories)