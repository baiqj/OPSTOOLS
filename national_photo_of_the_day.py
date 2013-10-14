import os
import urllib2
from BeautifulSoup import BeautifulSoup

html = BeautifulSoup(urllib2.urlopen("http://photography.nationalgeographic.com/photography/photo-of-the-day/").read())
tag = html.find('div',{'class':'download_link'}).find('a')
image_url = tag['href']

image = urllib2.urlopen(image_url).read()
image_name = 'media/national_wallpapers/' + image_url[image_url.rfind('/')+1:]
open(image_name, 'wb').write(image)
