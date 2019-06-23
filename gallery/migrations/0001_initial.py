# Generated by Django 2.1 on 2019-06-17 15:08

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
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('introduction', models.CharField(max_length=140)),
                ('picture', models.ImageField(upload_to='%Y/%m/%d/')),
                ('is_public', models.IntegerField(default=1)),
                ('write_time', models.DateTimeField()),
                ('is_delete', models.IntegerField(default=0)),
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
            model_name='pic',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.Type'),
        ),
    ]