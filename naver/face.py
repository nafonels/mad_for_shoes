import urllib2  
from bs4 import BeautifulSoup  
import re  
  
urls = [("Facebook", "https://itunes.apple.com/us/app/facebook/id284882215?mt=8")]
for name, url in urls:  
    print( "Progran: %s   Latest Version: ") % name,  
    response = urllib2.urlopen(url)  
    html_string = response.read()  
  
    soup = BeautifulSoup(html_string)  
    for li in soup.find_all('li'):  
        s = li.find('span')  
        if not (s and s.string):  
            continue  
        if s.string.strip() == 'Version:':  
            m = re.search('<\/span>(.*)<\/li>', str(li))  
            if m:  
                print m.group(1)
