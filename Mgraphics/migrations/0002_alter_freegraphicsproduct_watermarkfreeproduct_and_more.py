# Generated by Django 4.0.3 on 2022-04-06 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mgraphics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freegraphicsproduct',
            name='watermarkfreeproduct',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='paidgraphicsproduct',
            name='watermarkfreeproduct',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='paidgraphicsproduct',
            name='watermarkproduct',
            field=models.URLField(null=True),
        ),
    ]
