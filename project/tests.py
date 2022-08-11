from django.test import TestCase
from django.db.models import QuerySet
from project.models import Weather, Yield, Statistic
# Import to Random K dates in Range
from datetime import date, timedelta
import random


def populate_weather():
    # Set 3 random states
    states = [1, 2, 3]
    # initializing dates ranges
    start_date, end_date = date(2015, 12, 1), date(2015, 12, 31)
    # Make a list of dates to select random dates
    res_dates = [start_date]
    # put all dates from range to list
    while start_date != end_date:
        start_date += timedelta(days=1)
        res_dates.append(end_date)
    # random 20 dates from pack
    dates = random.choices(res_dates, k=20)
    for state in states:
        for inv_date in dates:
            # Random temperature for max/min
            max_temp = round(random.uniform(-40.00, 40.00), 2)
            min_temp = round(random.uniform(-40.00, 40.00), 2)
            # Check if random min_temp is bigger than max_temp
            while min_temp >= max_temp:
                min_temp = round(random.uniform(-40.00, 40.00), 2)
            # Random cm for rain amount
            rain_depth = round(random.uniform(0.00, 99.00), 2)
            # Create random weather data and save
            weather_data = Weather(state=state, date=inv_date, max_temp=max_temp, min_temp=min_temp, rain_depth=rain_depth)
            weather_data.save()
    # Return random generated objects
    return Weather.objects.all(), dates


class WeatherTestCase(TestCase):
    # Choose database what will use, for normal use, it is default
    databases = ["default"]
    # Define variables what will use to test
    states = [1, 2, 3]
    weather_list: QuerySet[Weather]
    dates = []

    def setUp(self):
        # Define random generated Weather model with data
        self.weather_list, self.dates = populate_weather()

    def test_weather_search(self):
        # Prepare random state ID and date to search
        state = random.choice(self.states)
        search_date = random.choice(self.dates)
        # Search and get data from random generated and existing Weather Model
        db_data = Weather.objects.filter(state=state, date=search_date).order_by('state')
        manual_data = self.weather_list.filter(state=state, date=search_date).order_by('state')
        # Check if two querysets(data list) are equal or not
        self.assertQuerysetEqual(db_data, manual_data)


class StatisticsTestCase(TestCase):
    # Choose database what will use, for normal use, it is default
    databases = ["default"]
    # Define variables what will use to test
    states = [1, 2, 3]
    year = 2015
    weather_list: QuerySet[Weather]
    statistics: QuerySet[Statistic]
    dates = []

    def setUp(self):
        # Define random generated Weather model with data
        self.weather_list, self.dates = populate_weather()
        for state in self.states:
            data_collection = self.weather_list.filter(state=state).values()
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
            if not Statistic.objects.filter(year=self.year, state=state).exists():
                # create a new record and save
                new_st = Statistic(year=self.year, state=state, avg_max_temp=avg_max_temp, avg_min_temp=avg_min_temp, total_prec=total_prec)
                new_st.save()
        self.statistics = Statistic.objects.all()

    def test_weather_search(self):
        # Prepare random state ID and date to search
        state = random.choice(self.states)
        # Search and get data from random generated and existing Weather Model
        db_data = Statistic.objects.filter(state=state, year=self.year).order_by('state')
        manual_data = self.statistics.filter(state=state, year=self.year).order_by('state')
        # Check if two querysets(data list) are equal or not
        self.assertQuerysetEqual(db_data, manual_data)