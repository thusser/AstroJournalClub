# Generated by Django 3.1.3 on 2020-11-12 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201111_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(verbose_name='First day of schedule.')),
                ('end', models.DateField(default='2100-12-31', verbose_name='Last day of schedule.')),
                ('time', models.TimeField(verbose_name='Starting time of meeting.')),
                ('duration', models.FloatField(verbose_name='Duration of meeting in hours.')),
                ('frequency', models.CharField(max_length=50, verbose_name='Frequency of schedule in iCal notation.')),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='date',
            field=models.DateField(db_index=True, verbose_name='Date of submission.'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time of vote.'),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Date and time of meeting.')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schedule')),
            ],
        ),
        migrations.AddField(
            model_name='vote',
            name='meeting',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.meeting'),
            preserve_default=False,
        ),
    ]
