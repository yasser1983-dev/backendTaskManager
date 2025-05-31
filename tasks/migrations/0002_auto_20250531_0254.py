from django.db import migrations
import uuid


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('tasks', 'Category')
    names = ['Trabajo', 'Estudio', 'Casa', 'Familia', 'Diversión']
    colors = ['#E53935', '#8E24AA', '#3949AB', '#039BE5', '#43A047']

    for name, color in zip(names, colors):
        Category.objects.get_or_create(name=name, defaults={'color': color})


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_categories),
    ]
