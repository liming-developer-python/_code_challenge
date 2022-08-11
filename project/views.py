from django.shortcuts import render, redirect
from project.models import Weather, Yield, Statistic
from django.core.paginator import Paginator


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
