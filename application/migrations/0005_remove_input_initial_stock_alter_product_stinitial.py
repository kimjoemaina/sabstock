# Generated by Django 4.2 on 2023-05-04 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_input_bonrecept_input_comments_input_numerocon_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='initial_stock',
        ),
        migrations.AlterField(
            model_name='product',
            name='stinitial',
            field=models.IntegerField(verbose_name='Stock Initial'),
        ),
    ]
