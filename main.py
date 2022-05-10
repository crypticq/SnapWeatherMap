import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
# from snaps import download_contents
from snaps import getSnaps
import sys
import re
import os


def get_lat_lon(city_name):
    try:

        geolocator = Nominatim(user_agent="SnapMaps")

        location = geolocator.geocode(city_name)

        # print(location.address)

        if location is not None:
            return {
                'city': city_name,
                'lat': location.latitude,
                'lon': location.longitude
            }

    except Exception as e:

        pass


east = ['Al Ahsa', 'Al ubaylah']


def get_city():
    r = requests.get('http://ncm.gov.sa/Ar/alert/Pages/feedalerts.aspx')
    soup = BeautifulSoup(r.content, 'lxml')
    i = 0
    len_city = len(soup.find_all('title'))
    print(" choise a number to fetch Data . ")
    for x in range(2, len_city):
        i += 1

        news = (soup.findAll('title')[x])
        print(i, news.text)

    try:

        num = int(input('Enter Number .'))
        if num > len_city:
            print('Your only allowd to choise from 1 to {}'.format(len_city))

            sys.clear()
            sys.exit()
        print("\033c", end="")

    except Exception as e:

        print('Enter a  Number. ')
        print('Exiting..')
        print(e)

    num += 2
    num -= 1
    news2 = soup.find_all('title')[num]
    city = news2.text
    city = city.split(',')[1]
    city = city.strip()
    print('.. .. . fetching Data from snapchat maps .. .. . ')
    print(get_lat_lon(city))
    lat = get_lat_lon(city)['lat']
    lon = get_lat_lon(city)['lon']

    print(getSnaps(lat,lon,city))


# print('[*] Found Total Of {} Alrets . [*] '.format(len_city))
# for city_name in soup.find_all('title'):
# 	names = city_name.text
# 	names = names.split(',')[1]
# 	rr = names.strip()
# 	if rr not in cities:
# 		cities.append(rr)


# if "Saudi Arabia" in cities:
# 	cities.remove('Saudi Arabia')
# if "Northern Borders" in cities:
# 	inde = cities.index('Northern Borders')
# 	cities[inde]= 'Turayf'
# if "Eastern" in cities:
# 	cities.remove('Eastern')
# 	cities.extend(east)

# for city in cities:
# 	try:
# 		lat = get_lat_lon(city)['lat']
# 		lon = get_lat_lon(city)['lon']
# 		getSnaps(lat,lon,city)

# 	except Exception as e:
# 		print(e)
# 		pass


get_city()