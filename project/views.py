from django.shortcuts import render, redirect
from project.models import Weather, Yield, Statistic
from django.core.paginator import Paginator
import datetime, glob, re


# Redirect into API when homepage calls
def home(request):
    return redirect(api_weather)


# Get Weather data with filtering
def api_weather(request):
    # Check if search option set or not
    if request.method == "POST":
        state_id = request.POST["state_id"]
        date = request.POST["date"]
        # Check if stateID and date filtering has defined
        if not state_id and not date:
            result = Weather.objects.all()
        else:
            if not date:
                result = Weather.objects.filter(state=state_id)
            elif not state_id:
                result = Weather.objects.filter(date=date)
            else:
                result = Weather.objects.filter(date=date, state=state_id)
    else:
        # When GET request, return all data without Filtering
        result = Weather.objects.all()
    # Pagination setting with 30 records for one page
    paginator = Paginator(result, per_page=30)
    # Count the number of pages
    page_number = request.GET.get('page')
    # Send result Query with pagination settings
    page_obj = paginator.get_page(page_number)
    return render(request, 'weather.html', {'page_obj': page_obj})


# Get Yield data
def api_yield(request):
    # GET and show yield data(has less data than others)
    result = Yield.objects.all()
    paginator = Paginator(result, per_page=30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'yield.html', {'page_obj': page_obj})


# GET statistics data with Filtering
def api_weather_stat(request):
    # Check if search option set or not
    if request.method == "POST":
        state_id = request.POST["state_id"]
        year = request.POST["year"]
        # Check if stateID and Year filtering has defined
        if not state_id and not year:
            result = Statistic.objects.all()
        else:
            if not year:
                result = Statistic.objects.filter(state=state_id)
            elif not state_id:
                result = Statistic.objects.filter(year=year)
            else:
                result = Statistic.objects.filter(year=year, state=state_id)
    else:
        # When GET request, return all data without Filtering
        result = Statistic.objects.all()
    # Pagination setting with 30 records for one page
    paginator = Paginator(result, per_page=10)
    # Count the number of pages
    page_number = request.GET.get('page')
    # Send result Query with pagination settings
    page_obj = paginator.get_page(page_number)
    return render(request, 'weather_stat.html', {'page_obj': page_obj})


# Action for update database
def update_yield():
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
                new_yd = Yield(year=year, amount=amount)
                new_yd.save()


def update_weather():
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
                # Check if data is indicated then 0 to make no change for avg/sum value
                if max_temp < -999:
                    max_temp = None
                if min_temp < -999:
                    min_temp = None
                if rain_depth < -999:
                    rain_depth = None
                # Check if database has already same record(Even it is first, migrate action can take on several times)
                if not Weather.objects.filter(date=date, state=state).exists():
                    # create a new record and save
                    new_weather = Weather(date=date, state=state, max_temp=max_temp, min_temp=min_temp, rain_depth=rain_depth)
                    new_weather.save()
                # update the record when it is indicated for the first input
                elif max_temp is None or min_temp is None or rain_depth is None:
                    # date and state should not be changed so just update others
                    Weather.objects.filter(date=date, state=state).update(max_temp=max_temp, min_temp=min_temp, rain_depth=rain_depth)


# Calculate statistic data from already input data from 0002
def get_statistics():
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
            max_temp_length, min_temp_length = len(data_collection), len(data_collection)
            for data in data_collection:
                if data['max_temp']:
                    sum_max_temp += data['max_temp']
                else:
                    max_temp_length -= 1
                if data['min_temp']:
                    sum_min_temp += data['min_temp']
                else:
                    min_temp_length -= 1
                if data['rain_depth']:
                    total_prec += data['rain_depth']
            # Get average values for stateID and year(When it is not available put None value
            try:
                avg_max_temp = sum_max_temp / max_temp_length
            except:
                avg_max_temp = None
            try:
                avg_min_temp = sum_min_temp / min_temp_length
            except:
                avg_min_temp = None

            # check if same records already exists then add new one
            if not Statistic.objects.filter(year=year, state=state).exists():
                # create a new record and save
                new_st = Statistic(year=year, state=state, avg_max_temp=avg_max_temp, avg_min_temp=avg_min_temp, total_prec=total_prec)
                new_st.save()
            # update the record when it is indicated for the first input
            elif avg_max_temp is None or avg_min_temp is None:
                # year and state should not be changed so just update others
                Weather.objects.filter(year=year, state=state).update(avg_max_temp=avg_max_temp, avg_min_temp=avg_min_temp, total_prec=total_prec)


# Update Database POST
def update_data(request):
    # check and update database one by one following the input steps
    update_yield()
    update_weather()
    # update statistics table also
    get_statistics()
    # After finish just return to API home page
    return redirect(api_weather)
