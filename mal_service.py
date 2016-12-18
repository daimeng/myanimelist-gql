import urllib2
import base64
import xml.etree.ElementTree as ET
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read("auth.ini")
user = parser.get('auth_info', 'username')
passw = parser.get('auth_info', 'password')


# TODO: implement some kind of caching
def get_list(username=user):
    url = "http://myanimelist.net/malappinfo.php?u=%s&status=all&type=anime" % username
    req = urllib2.Request(url)
    b64string = base64.encodestring('%s:%s' % (username, passw)).replace('\n', '')
    req.add_header("Authorization", "Basic %s" % b64string)
    resp = urllib2.urlopen(req)
    return ET.fromstring(resp.read())
