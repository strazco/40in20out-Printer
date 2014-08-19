from xml.dom import minidom
import urllib

#url_str = 'http://www.newyorkfed.org/markets/omo/dmm/fftoXML.cfm?type=daily'
url_str = 'http://40in20out.com/subscribers/messages2.xml'
xml_str = urllib.urlopen(url_str).read()
xmldoc = minidom.parseString(xml_str)

action = xmldoc.getElementsByTagName('VFPData')
# prints the first base:OBS_VALUE it finds
print action[0].firstChild.nodeValue

# prints the second base:OBS_VALUE it finds
print action[1].firstChild.nodeValue

# prints all base:OBS_VALUE in the XML doc
for obs_val in action:
    print obs_val.firstChild.nodeValue
