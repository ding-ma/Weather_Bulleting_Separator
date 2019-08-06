import re
import urllib.request

for i in range(1, 6):
    url = "https://dd.weather.gc.ca/bulletins/alphanumeric/2019080" + str(i) + "/FL/CWUL/19/"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    page = str(the_page)
    flcn41 = re.compile(">FLCN41_CWUL")
    flcnURl = re.compile("FLCN41_CWUL_.*<")
    for bulletin in flcn41.finditer(page):
        print(page[bulletin.start() + 1:bulletin.end() + 15])
