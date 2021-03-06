# Generated by Django 3.1.3 on 2020-11-06 18:43

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
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Name of author')),
                ('url', models.CharField(max_length=100, verbose_name='arXiv URL')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=15, verbose_name='Category name')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, max_length=10, verbose_name='arXiv identifier')),
                ('date', models.DateField(verbose_name='Date of submission.')),
                ('number', models.IntegerField(verbose_name='arXiv post number on day')),
                ('title', models.CharField(max_length=100, verbose_name='Title of publication')),
                ('url', models.CharField(max_length=100, verbose_name='arXiv URL')),
                ('summary', models.TextField(verbose_name='Summary')),
                ('authors', models.ManyToManyField(to='main.Author')),
                ('categories', models.ManyToManyField(to='main.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='Time of vote')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.publication')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
