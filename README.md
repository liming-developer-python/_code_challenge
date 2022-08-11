# _code_challenge
Django Weather | Crop Analysis API

###### 1. First install Python and venv for the project.

After install Python, go to project directory then run commands to install virtual environment.(It doesn't have to be venv, but I usually prefer venv for django project)

```
# work via terminal/command prompt
pip3 install virtualenv

# Go to directory 
python3 -m venv path\to\venv

# Usually on the top directory of the project
python3 -m venv venv

# install django
pip3 install django
```

Then you finished install virtual environment and django for the project.

## Please skip step 2 for the quick test Because migrate takes a long time to finish. There are more than 200000 records to insert.
###### 2. Run migrations to set database (used sqlite) 
```
python manage.py migrate
```
Usually starts with ```python manage.py makemigrations```, but already made it and also make dump actions to migrates so please skip for ```makemigrations``` actions.

###### It takes a while so I suggest to use small txt files for input(especially reduce from wx_data)

## Skip step 2 and Directly Run server and Test Units.
###### 3. Finally run the server
```
python3 manage.py runserver
```

Then you can check on ```http://localhost:8000``` normally.
You can set your own port number like  ``` python3 manage.py runserver 8888```.

###### 4. Reference -- Unit Test Case 
To test all cases together, run following command
```
python3 manage.py test
```

To test individual testcases, there are 2 cases for weather API and stats API
```
python3 manage.py test project.tests.WeatherTestCase
python3 manage.py test project.tests.StatisticsTestCase
```
## Thanks for your feedback!
