# Generated by Django 2.1 on 2019-06-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190613_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='is_delete',
            field=models.IntegerField(default=0),
        ),
    ]
