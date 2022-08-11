import re


with open('project/data/yld_data/US_corn_grain_yield.txt', 'r') as f:
    yield_data = f.readlines()
    for line in yield_data:
        year = re.split("\t|\n| ", line)[0]
        amount = re.split("\t|\n| ", line)[1]
        print(year, amount)
