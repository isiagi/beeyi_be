# yourapp/management/commands/seed_categories.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from category.models import Category

class Command(BaseCommand):
    help = 'Seeds the database with predefined categories and subcategories'

    def create_category(self, name, description="", parent=None):
        slug = slugify(name)
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={
                'description': description,
                'parent': parent,
                'slug': slug
            }
        )
        return category

    def handle(self, *args, **kwargs):
        # Define the category structure
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Electronic devices and accessories',
                'subcategories': [
                    {
                        'name': 'Smartphones',
                        'description': 'Mobile phones and accessories',
                        'subcategories': [
                            {'name': 'Android Phones'},
                            {'name': 'iPhones'},
                            {'name': 'Phone Cases'},
                            {'name': 'Chargers'}
                        ]
                    },
                    {
                        'name': 'Laptops',
                        'description': 'Portable computers',
                        'subcategories': [
                            {'name': 'Gaming Laptops'},
                            {'name': 'Business Laptops'},
                            {'name': 'Chromebooks'}
                        ]
                    },
                    {
                        'name': 'Tablets',
                        'subcategories': [
                            {'name': 'iPads'},
                            {'name': 'Android Tablets'}
                        ]
                    },
                    {'name': 'Accessories'}
                ]
            },
            {
                'name': 'Fashion',
                'description': 'Clothing and accessories',
                'subcategories': [
                    {
                        'name': "Men's Clothing",
                        'subcategories': [
                            {'name': 'Shirts'},
                            {'name': 'Pants'},
                            {'name': 'Suits'}
                        ]
                    },
                    {
                        'name': "Women's Clothing",
                        'subcategories': [
                            {'name': 'Dresses'},
                            {'name': 'Tops'},
                            {'name': 'Skirts'}
                        ]
                    },
                    {'name': 'Shoes'},
                    {'name': 'Accessories'}
                ]
            },
            {
                'name': 'Home & Garden',
                'description': 'Home improvement and garden supplies',
                'subcategories': [
                    {
                        'name': 'Furniture',
                        'subcategories': [
                            {'name': 'Living Room'},
                            {'name': 'Bedroom'},
                            {'name': 'Office'}
                        ]
                    },
                    {'name': 'Decor'},
                    {'name': 'Kitchen'},
                    {'name': 'Outdoor'}
                ]
            },
            {
                'name': 'Sports',
                'description': 'Sports equipment and gear',
                'subcategories': [
                    {'name': 'Equipment'},
                    {'name': 'Clothing'},
                    {'name': 'Footwear'},
                    {'name': 'Accessories'}
                ]
            },
            {
                'name': 'Pets',
                'description': 'Pet supplies and accessories',
                'subcategories': [
                    {
                        'name': 'Dogs',
                        'subcategories': [
                            {'name': 'Food'},
                            {'name': 'Toys'},
                            {'name': 'Accessories'},
                            {'name': 'Health & Wellness'}
                        ]
                    },
                    {
                        'name': 'Cats',
                        'subcategories': [
                            {'name': 'Food'},
                            {'name': 'Litter & Accessories'},
                            {'name': 'Toys'},
                            {'name': 'Health & Wellness'}
                        ]
                    },
                    {
                        'name': 'Fish',
                        'subcategories': [
                            {'name': 'Aquariums'},
                            {'name': 'Food'},
                            {'name': 'Decorations'}
                        ]
                    },
                    {
                        'name': 'Birds',
                        'subcategories': [
                            {'name': 'Cages'},
                            {'name': 'Food'},
                            {'name': 'Toys'}
                        ]
                    },
                    {
                        'name': 'Small Pets',
                        'subcategories': [
                            {'name': 'Habitats'},
                            {'name': 'Food'},
                            {'name': 'Accessories'}
                        ]
                    }
                ]
            }
        ]

        def create_subcategories(parent_category, subcategories_data):
            for subcat_data in subcategories_data:
                subcategory = self.create_category(
                    name=subcat_data['name'],
                    description=subcat_data.get('description', ''),
                    parent=parent_category
                )
                if 'subcategories' in subcat_data:
                    create_subcategories(subcategory, subcat_data['subcategories'])

        # Create all categories
        for category_data in categories_data:
            category = self.create_category(
                name=category_data['name'],
                description=category_data.get('description', '')
            )
            if 'subcategories' in category_data:
                create_subcategories(category, category_data['subcategories'])

        self.stdout.write(self.style.SUCCESS('Successfully seeded categories'))