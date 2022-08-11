from django.db import migrations
import datetime
import logging

logger = logging.getLogger(__name__)


# Calculate statistic data from already input data from 0002
def get_statistics(apps, schema_editor):
    # Get model definition form app
    Weather = apps.get_model('project', 'Weather')
    Yield = apps.get_model('project', 'Yield')
    Statistic = apps.get_model('project', 'Statistic')
    # Get existing range of years, list of states(ID) from database
    year_list = Yield.objects.values_list('year', flat=True)
    state_list = Weather.objects.values_list('state', flat=True)
    # Sum and Avg by state and year
    for state in state_list:
        for year in year_list:
            # Set date range (ex: 1985.1.1 - 1985.12.31)
            start = datetime.date(year, 1, 1)
            # Last date in range is not included
            end = datetime.date(year + 1, 1, 1)
            # Get filtered records with stateID and date range
            data_collection = Weather.objects.filter(date__range=[start, end], state=state).values()
            # Sum all info from got collection
            sum_max_temp, sum_min_temp, total_prec = 0, 0, 0
            for data in data_collection:
                sum_max_temp += data['max_temp']
                sum_min_temp += data['min_temp']
                total_prec += data['rain_depth']
            # Get average values for stateID and year
            avg_max_temp = sum_max_temp / len(data_collection)
            avg_min_temp = sum_min_temp / len(data_collection)
            # check if same records already exists then add new one
            if not Statistic.objects.filter(year=year, state=state).exists():
                # create a new record and save
                logger.debug("New Statistics data has created")
                new_st = Statistic(year=year, state=state, avg_max_temp=avg_max_temp, avg_min_temp=avg_min_temp, total_prec=total_prec)
                new_st.save()
    logger.debug("Statistics finished Calculation")


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20220811_0933'),
    ]

    operations = [
        migrations.RunPython(get_statistics),
    ]
