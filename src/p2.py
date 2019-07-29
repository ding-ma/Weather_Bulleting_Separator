import csv
import re

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

# for dates
for ind, val in enumerate(starlst):
    for r in riskList:
        if ind < len(starlst) - 1:
            first = starlst[ind]
            second = starlst[ind + 1]
            if first.end() <= r.start() <= second.start():
                pass
                # print(first.end(), r.start(), second.start())
    else:
        pass
        # print(starlst[ind].end())

locationset = set()


def resetSet():
    for q in locationlst:
        locationset.add(q.group(0))


resetSet()

for element in locationset:
    for matches in locationlst:
        if element == matches.group(0):
            print(matches)
