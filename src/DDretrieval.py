import os
import re
import shutil
import smtplib
import urllib.error
import urllib.request
from datetime import datetime, timedelta

path = "/fs/home/fs1/eccc/oth/airq_central/sair001/public_html/bulletin_infoSmog/"
if os.path.exists(path + "tempdir"):
    shutil.rmtree(path + "tempdir")
    os.mkdir(path + "tempdir")
else:
    os.mkdir(path + "tempdir")


def sendemail(errormsg):
    sender = 'InfoSmog-FLCN41-Process'
    receivers = ['ding.ma@canada.ca']

    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, errormsg)


today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime("%Y%m%d")
url = "https://dd.weather.gc.ca/bulletins/alphanumeric/" + yesterday + "/FL/CWUL/"
request = urllib.request.Request(url)
resp = urllib.request.urlopen(request)
hourpage = str(resp.read())
findalldigits = re.compile(">\d{2}")
flcn41 = re.compile(">FLCN41_CWUL_")
hlst = []
for hourdigit in findalldigits.finditer(hourpage):
    urlwithhour = url + hourdigit.group()[1:]
    req = urllib.request.Request(urlwithhour)
    response = urllib.request.urlopen(req)
    bulletinpage = str(response.read())
    for bulletin in flcn41.finditer(bulletinpage):
        hlst.append(bulletin)
        download = bulletinpage[bulletin.start() + 1:bulletin.end() + 22].split("<")
        downloadurl = urlwithhour + "/" + download[0]
        try:
            urllib.request.urlretrieve(downloadurl,
                                       path + "tempdir/CWUL_FLCN41_" + yesterday + "_h_" + hourdigit.group()[
                                                                                           1:] + ".txt")
            urllib.request.urlretrieve(downloadurl,
                                       path + "datamart_downloads/CWUL_FLCN41_" + yesterday + "_h_" + hourdigit.group()[
                                                                                                      1:] + ".txt")
        except urllib.error.HTTPError:
            sendemail("Error occured while downloading FLCN41-CWUL for hour: " + hourdigit.group()[1:])

if len(hlst) < 2:
    sendemail("Less than 2 bulletins was downloaded for " + yesterday)

os.system("cd /home/ && /usr/bin/python3 /home/sair001/public_html/bulletin_infoSmog/script/infoSmogDailyScript.py")
