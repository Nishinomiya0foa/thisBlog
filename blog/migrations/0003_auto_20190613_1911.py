# Generated by Django 2.1 on 2019-06-13 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190613_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='write_time',
            field=models.DateTimeField(),
        ),
    ]
