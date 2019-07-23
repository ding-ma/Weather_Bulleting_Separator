import csv
import difflib
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

inputfile = open("bulletin.txt").read()
lines = inputfile.split("\n")
containsSmoke = "IN SMOKE."
containsStars = "*** "
containsEnd = "END"

smokelist = []
starlst = []
emptylist = []


def convertTime(dateStar):
    datetimeStar = dateStar.replace(",", "").split(" ")
    month = datetimeStar[1]
    day = datetimeStar[2]
    year = datetimeStar[3]
    hour = datetimeStar[4].replace("Z", "")
    from calendar import month_abbr
    for k, v in enumerate(month_abbr):
        if v == month:
            month = k
            break
    datetimeObject = datetime(int(year), int(month), int(day), int(hour.split(":")[0]), int(hour.split(":")[1]))
    return datetimeObject


for i in range(len(inputfile.split("\n"))):
    if containsSmoke in lines[i]:
        smokelist.append(i)
    if containsStars in lines[i]:
        starlst.append(i)
    if '' == lines[i]:
        emptylist.append(i)

paragraphlst = []
for o, p in zip(lines, range(len(lines))):
    if '' == o:
        paragraphlst.append(p)

f = open("output.txt", "w+")
for w in smokelist:
    toFindSmoke = w
    upperSpace = min([i for i in paragraphlst if i >= toFindSmoke], key=lambda x: abs(x - toFindSmoke))
    lowerSpace = min([i for i in paragraphlst if i < toFindSmoke], key=lambda x: abs(x - toFindSmoke))

    start = min([i for i in starlst if i < toFindSmoke], key=lambda x: abs(x - toFindSmoke))
    end = min([i for i in emptylist if i >= start], key=lambda x: abs(x - start))

    for z in lines[lowerSpace:upperSpace]:
        nameinList = difflib.get_close_matches(z, namelst, n=1, cutoff=.6)
        if len(nameinList) > 0:
            universalIndex = namelst.index(nameinList[0])
            print(sitelst[universalIndex], provincelst[universalIndex], z)
    reportLocation = lines[start + 1].split(" ")[1]
    if lines[start].startswith("*"):
        localtime = convertTime(lines[start].replace("*", ""))
        lines[start] = localtime.strftime("%Y/%m/%d %H:%M:00 %p")

    for a in lines[start:end]:
        f.write(a)
        f.write("\n")
    for b in lines[lowerSpace:upperSpace + 1]:
        f.write(b)
        f.write("\n")
    f.write("\n")
