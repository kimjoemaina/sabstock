# Generated by Django 4.2 on 2023-04-23 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_alter_input_options_alter_output_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constructionsite',
            options={'permissions': [('export_constructionsite', 'Can export Construction Site'), ('see_dashboard', 'Can See Dashboard')]},
        ),
    ]