# Generated by Django 2.1 on 2019-06-20 11:04

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_articles_is_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
