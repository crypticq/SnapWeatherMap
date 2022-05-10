import requests, time, argparse, os, json
import sys


def download_contents(data, city_name):
    i = 0
    l = len(data["manifest"]["elements"])
    print("Downloading " + str(l) + " media items")
    for value in data["manifest"]["elements"]:

        idnum = value['id']
        info = value['snapInfo']
        info = value['snapInfo']
        media = info.get('streamingMediaInfo')
        preview_url = None
        media_url = None
        #	    overlay_url = None
        if media:
            if media.get('previewUrl'):
                preview_url = media['prefixUrl'] + media['previewUrl']
                with open('Media-Snap-Map/' + str(city_name) + str(i) + ".jpg", "wb") as f:
                    f.write(requests.get(preview_url).content)
            if media.get('mediaUrl'):
                media_url = media['prefixUrl'] + media['mediaUrl']
                with open('Media-Snap-Map/' + str(i) + str(city_name) + ".mp4", "wb") as f:
                    f.write(requests.get(media_url).content)
            # if media.get('overlayUrl'):
            #     overlay_url = media['prefixUrl'] + media['overlayUrl']
            #     with open('Media-Snap-Map/'+ str(idnum) + ".png", "wb") as f:
            #         f.write(requests.get(overlay_url).content)

        i += 1


RADIUS = "15000"


def getEpoch():
    return requests.post('https://ms.sc-jpl.com/web/getLatestTileSet', headers={'Content-Type': 'application/json'},
                         data='{}').json()['tileSetInfos'][1]['id']['epoch']


def getSnaps(lat, lon , city ):
    """
    POST https://ms.sc-jpl.com/web/getPlaylist HTTP/1.1
    Content-Type: application/json

    {"requestGeoPoint":{"lat":LATITUDE,"lon":LONGITUDE},"tileSetId":{"flavor":"default","epoch":EPOCH,"type":1},"radiusMeters":RADIUS}
    """
    Epoch = getEpoch()
    dataPost = '{"requestGeoPoint":{"lat":' + str(lat) + ',"lon":' + str(
        lon) + '},"tileSetId":{"flavor":"default","epoch":' + Epoch + ',"type":1},"radiusMeters":' + RADIUS + '}'
    responseSnaps = requests.post('https://ms.sc-jpl.com/web/getPlaylist', headers={'Content-Type': 'application/json'},
                                  data=dataPost)

    data = responseSnaps.json()
    try:
        download_contents(data,city)

        return data
    except json.decoder.JSONDecodeError:
        raise ('No snaps found ..')
