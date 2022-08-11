# Generated by Django 4.1 on 2022-08-10 16:28

from django.db import migrations, models
# additional models to read txt data
import re


def input_yield(apps, schema_editor):
    Yield = apps.get_model('project', 'Yield')
    with open('../data/yld_data/US_corn_grain_yield.txt', 'r') as f:
        yield_data = f.readlines()
        for line in yield_data:
            year = re.split("\t|\n| ", line)[0]
            amount = re.split("\t|\n| ", line)[1]
            print(year, amount)
            # person.name = '%s %s' % (person.first_name, person.last_name)
            # person.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [('migrations', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('max_temp', models.FloatField()),
                ('min_temp', models.FloatField()),
                ('rain_depth', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Yield',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('amount', models.IntegerField()),
            ],
        ),
    ]