from django.db import migrations

def create_default_categories(apps, schema_editor):
    Category = apps.get_model('farmers', 'Category')
    categories = ['Плодове', 'Зеленчуци', 'Млечни продукти', 'Месо', 'Хляб']
    for name in categories:
        Category.objects.get_or_create(name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('farmers', '0003_category_product_category'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
