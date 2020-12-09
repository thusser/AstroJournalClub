# Generated by Django 3.1.3 on 2020-12-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201112_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='meeting',
        ),
        migrations.AddField(
            model_name='vote',
            name='present',
            field=models.BooleanField(default=False, verbose_name='Whether user wants to present paper.'),
        ),
        migrations.DeleteModel(
            name='Meeting',
        ),
    ]