from xml.dom import minidom
import urllib

url_str = 'http://www.newyorkfed.org/markets/omo/dmm/fftoXML.cfm?type=daily'
xml_str = urllib.urlopen(url_str).read()
xmldoc = minidom.parseString(xml_str)

obs_values = xmldoc.getElementsByTagName('base:OBS_VALUE')
# prints the first base:OBS_VALUE it finds
# print obs_values[0].firstChild.nodeValue

# prints the second base:OBS_VALUE it finds
# print obs_values[1].firstChild.nodeValue

# prints all base:OBS_VALUE in the XML doc
for obs_val in obs_values:
    print obs_val.firstChild.nodeValue
