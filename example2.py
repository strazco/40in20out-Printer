from lxml import etree
from io import StringIO
import urllib

url = 'http://www.newyorkfed.org/markets/omo/dmm/fftoXML.cfm?type=daily'
root = etree.parse(urllib.urlopen(url))

for obs in root.xpath('/ff:DataSet/ff:Series/ff:Obs'):
    price = obs.xpath('./base:OBS_VALUE').text
    print(price)
