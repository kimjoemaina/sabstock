# Generated by Django 4.2 on 2023-05-25 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_remove_input_initial_stock_constructionpermission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=125, verbose_name='Désignation'),
        ),
        migrations.AlterField(
            model_name='constructionsite',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nom du chantier'),
        ),
        migrations.AlterField(
            model_name='input',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_inputs', to='application.product', verbose_name='Produit'),
        ),
        migrations.AlterField(
            model_name='output',
            name='exit_coupon',
            field=models.IntegerField(verbose_name='N° Bon de sortie'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=155, verbose_name='Désignation'),
        ),
    ]
