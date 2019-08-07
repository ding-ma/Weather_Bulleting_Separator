import re
import urllib.request
from datetime import datetime, timedelta

today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime("%Y%m%d")
hourslst = ["08", "19"]
for h in hourslst:
    url = "https://dd.weather.gc.ca/bulletins/alphanumeric/" + yesterday + "/FL/CWUL/" + h + "/"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    page = str(the_page)
    flcn41 = re.compile(">FLCN41_CWUL")
    for bulletin in flcn41.finditer(page):
        pageULR = url + page[bulletin.start() + 1:bulletin.end() + 15]
        req1 = urllib.request.Request(pageULR)
        response1 = urllib.request.urlopen(req1)
        the_page1 = response1.read()
        urllib.request.urlretrieve(pageULR, "downloads/CWUL_FLCN41_" + yesterday + "_h_" + h + ".txt")
