import requests
from PIL import Image
from StringIO import StringIO

url = 'https://api.instagram.com/v1/tags/foorporn/media/recent?access_token=14190.f59def8.985b0fbb945344acbb3f8ec0bdbe0fab'
r = requests.get(url)
counter=0
for data in r.json['data']:
    url = data['images']['standard_resolution']['url']
    img = requests.get(url)
    i = Image.open(StringIO(img.content))
    i.save("img_%d.png" % counter)
    counter += 1