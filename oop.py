import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import sys
import concurrent.futures
import re
import os


cit = []
mp4 = []


class snap_data:
    def __init__(self,  city=None ):
        self.rad = 5000
        self.mp4x = []
        self.city = city

    def getEpoch(self):
        return requests.post('https://ms.sc-jpl.com/web/getLatestTileSet', headers={'Content-Type': 'application/json'},
                             data='{}').json()['tileSetInfos'][1]['id']['epoch']

    def getSnaps(self):
        try:
            e = self.getEpoch()
            url = "https://ms.sc-jpl.com:443/web/getPlaylist"
            lat = self.get_lat_lon()
            lat = lat['lat']
            lon = self.get_lat_lon()
            lon = lon['lon']
            json_data = {
                'requestGeoPoint': {
                    'lat': lat,
                    'lon': lon,
                },
                'tileSetId': {
                    'flavor': 'default',
                    'epoch': e,
                    'type': 1,
                },
                'radiusMeters': 15000,
            }

            r = requests.post(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0'},
                              json=json_data)


            data = r.json()
            for value in data["manifest"]["elements"]:

                info = value['snapInfo']

                media = info.get('streamingMediaInfo')
                if media:
                    if media.get('mediaUrl'):
                        media_url = media['prefixUrl'] + media['mediaUrl']

                        self.mp4x.append(media_url)
        except Exception as e:
            print('No Data , Try Another City .. ')
            pass

        return self.mp4x


    def get_lat_lon(self):

        try:

            geolocator = Nominatim(user_agent="SnapMaps")

            location = geolocator.geocode(self.city)

            # print(location.address)

            if location is not None:
                self.lat = location.latitude
                self.lon = location.longitude


                return {
                    'city':self.city ,
                    'lat': self.lat,
                    'lon': self.lon
                }

        except Exception as e:

            pass

    def get_city(self):
        global cit_name
        cit_name = []
        r = requests.get('http://ncm.gov.sa/Ar/alert/Pages/feedalerts.aspx')
        soup = BeautifulSoup(r.content, 'lxml')
        i = 0
        len_city = len(soup.find_all('title'))
        print(" Chose a number to fetch Data . ")
        for x in range(2, len_city):
            i += 1

            news = (soup.findAll('title')[x])
            print(i, news.text)

        try:

            num = int(input('Enter Number .'))
            if num > len_city:
                print('Your only allowd to choise from 1 to {}'.format(len_city))
                sys.exit()

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
        self.city = city
        cit.append(city)

        print('.. .. . fetching Data from snapchat maps .. .. . ')
        print('Geeting The Data from {}'.format(city))
        print(city)




    
    
    






# if __name__ == '__main__':
#
#     x = snap_data('taif')

def dow(url):
    r = requests.get(url)
    name = r.url.split('/')[3]
    x = name.split('=')[0]
    file_name = ('Yazeed/{}_{}.mp4'.format(cit[0],x))
    with open(file_name , 'wb') as f:
        f.write(r.content)

    print('Done DOwnloading  {}'.format(file_name))


if __name__ == "__main__":

    x = snap_data('2')
    x.get_city()
    mp = x.getSnaps()
    for i in mp:
        try:
            mp4.append(i)
        except:
            pass


    for x in mp4:
        dow(x)


















