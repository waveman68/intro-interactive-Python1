__author__ = 'Sam Broderick'

import time

seconds_in_year = 3600 * 24 * 365
print(seconds_in_year)

time_now = time.time()
print(time_now)

print('Years')
print(time_now // seconds_in_year)
print(2016 - time_now // seconds_in_year)

print('Fraction Remainder')
print(time_now % seconds_in_year)
