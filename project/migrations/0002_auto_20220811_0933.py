from django.db import migrations
# additional models to read txt data
import re
import glob
import datetime
import logging

logger = logging.getLogger(__name__)


# Define dump actions while migrating a new database
# read txt files and save initial input
def input_yield(apps, schema_editor):
    # Get model definition form app
    Yield = apps.get_model('project', 'Yield')
    # Read txt file line by line and create new instances
    with open('project/data/yld_data/US_corn_grain_yield.txt', 'r') as f:
        yield_data = f.readlines()
        # Read lines one by one
        for line in yield_data:
            # Separate data and get individual info
            year = re.split("\t|\n| ", line)[0]
            amount = re.split("\t|\n| ", line)[1]
            # Check if database has already same record(Even it is first, migrate action can take on several times)
            if not Yield.objects.filter(year=year, amount=amount).exists():
                # create a new record and save
                logger.debug('New Yield record has created')
                new_yd = Yield(year=year, amount=amount)
                new_yd.save()
    logger.debug("Yield Model created with data correctly")


def input_weather(apps, schema_editor):
    # Get model definition form app
    Weather = apps.get_model('project', 'Weather')
    # Read all txt files
    txt_files = glob.glob('project/data/wx_data/*.txt')
    for file in txt_files:
        # Find state ID from txt file's name
        state = int(file.split('USC')[1][:4])
        with open(file, 'r') as f:
            # Read txt file line by line and create new instances
            weather_data = f.readlines()
            for line in weather_data:
                # Separate data and get individual info
                date_str = re.split("\t|\n", line)[0]
                date = datetime.date(int(date_str[0:4]), int(date_str[4:6]), int(date_str[6:]))
                # Get data with correct ones not tenth of number
                max_temp = int(re.split("\t|\n", line)[1].replace(" ", "")) / 10
                min_temp = int(re.split("\t|\n", line)[2].replace(" ", "")) / 10
                rain_depth = int(re.split("\t|\n", line)[3].replace(" ", "")) / 10
                # Check if database has already same record(Even it is first, migrate action can take on several times)
                if not Weather.objects.filter(date=date, state=state).exists():
                    # create a new record and save
                    logger.debug("New Weather info record has created")
                    new_weather = Weather(date=date, state=state, max_temp=max_temp, min_temp=min_temp, rain_depth=rain_depth)
                    new_weather.save()
    logger.debug("Weather Model created with data correctly")


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(input_yield),
        migrations.RunPython(input_weather),
    ]
