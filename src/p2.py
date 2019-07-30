import csv
import re
from datetime import datetime

siteconverter = open("nameToSite.csv")
reader = list(csv.reader(siteconverter))
sitelst = []
provincelst = []
namelst = []

for x in range(len(reader)):
    l = reader[x]
    site = l[0]
    province = l[1]
    name = l[2]
    sitelst.append(site)
    provincelst.append(province)
    namelst.append(name)

file = open("bulletin.txt", "r").read().strip()

nameToSiteAndProvDict = {
    i: [j, k] for i, j, k in zip(namelst, provincelst, sitelst)
}

riskList = []
riskPattern = re.compile("RISK EXCEPT")
for risk in riskPattern.finditer(file):
    riskList.append(risk)

starlst = []
datePattern = re.compile("\*\*\* ")
for star in datePattern.finditer(file):
    starlst.append(star)

locationlst = []
for name in namelst:
    locationPattern = re.compile(name)
    for loc in locationPattern.finditer(file):
        locationlst.append(loc)


casPrediction = []
for i in riskList:
    cas = re.findall("\d", file[i.start() - 30:i.end() + 25])
    if len(cas) > 2:
        c2 = cas[1]
        c3 = cas[2]
        c = c2 + c3
        cas.insert(1, c)
        del cas[2:4]
    casPrediction.append(cas)
    # print(cas)

locationset = set()


def resetSet():
    for q in locationlst:
        locationset.add(q.group(0))


resetSet()

out = open("tt.txt", "w+")


def convertTime(dateStar):
    datetimeStar = dateStar.replace(",", "").split(" ")
    month = datetimeStar[0]
    day = datetimeStar[1]
    year = datetimeStar[2]
    hour = datetimeStar[3].replace("Z", "")
    from calendar import month_abbr
    for k, v in enumerate(month_abbr):
        if v == month:
            month = k
            break
    datetimeObject = datetime(int(year), int(month), int(day), int(hour.split(":")[0]), int(hour.split(":")[1]))
    return datetimeObject.strftime("%Y/%m/%d %H:%M:%S"), datetimeObject.strftime("%p")


dayofweek = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def pairValuefinder(beforeperiod, time):
    preforecast = re.findall('TONIGHT|TODAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY', beforeperiod)
    forecast = preforecast[0]
    if time == "AM" and forecast == "TODAY":
        return "1"
    if time == "AM" and forecast == "TONIGHT":
        return "2"
    if time == "AM" and forecast in dayofweek:
        return "3"
    if time == "PM" and (forecast == "TONIGHT" or forecast == "TODAY"):
        return "4"
    if time == "PM" and forecast in dayofweek:
        return "5"


def returnStations(riskCharacterStart, riskCharacterEnd, date):
    for match in locationlst:

        if abs(match.end() - riskCharacterStart) < 100:
            pass
            forecast = file[riskCharacterStart - 60:riskCharacterEnd + 30]
            convertedTime = convertTime(file[date:date + 19])
            out.write(convertedTime[0] + convertedTime[1] + "\n")
            provandsite = nameToSiteAndProvDict[file[match.start():match.end()]]
            out.write(file[match.start():match.end()] + "," + provandsite[0].strip() + "," + provandsite[1] + "\n")
            cas = re.findall("\d", forecast)
            out.write("CASi: " + cas[0] + " CASe: " + cas[1] + "\n")
            valuePair = pairValuefinder(forecast, convertedTime[1])
            if valuePair != None:
                out.write("Paire: " + valuePair)
            out.write("\n---\n")
            out.write(file[match.start():match.end()] + "\n")
            out.write(forecast + "\n")
            out.write("----------------\n")

# for dates
for ind, val in enumerate(starlst):
    for r in riskList:
        if ind < len(starlst) - 1:
            first = starlst[ind]
            second = starlst[ind + 1]
            if first.end() <= r.start() <= second.start():
                pass
                riskToMatch = r.start()
                # print(first.end(), r.start(), second.start(),"\n")
                # print(file[r.start()-60:r.end()+50])
                returnStations(r.start(), r.end(), first.end())
                #print("------------------------")
    else:
        pass
        # print(starlst[ind].end())



for element in locationset:
    for matches in locationlst:
        if element == matches.group(0):
            pass
        # print(matches)
