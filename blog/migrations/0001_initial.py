# Generated by Django 2.1 on 2019-06-13 15:39

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('write_time', models.DateTimeField(auto_created=datetime.datetime(2019, 6, 13, 15, 39, 23, 809636))),
                ('title', models.CharField(max_length=40)),
                ('content', ckeditor.fields.RichTextField()),
                ('is_public', models.IntegerField(default=1)),
                ('views', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Type'),
        ),
    ]
