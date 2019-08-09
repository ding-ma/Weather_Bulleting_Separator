import csv
import datetime
import os
import re
import xml.etree.ElementTree as ET

# cleans up xml file from the junk underneath.
a = re.compile("-.-.-.-.-.-.-.-.-.-.-.-.-")
templst = []
for file in os.listdir("process"):
    f = open("process/" + file, "r")
    fread = f.read()
    for b in a.finditer(fread):
        fout = open("a/" + file, "w+")
        fout.write(fread[:b.start()])


# reads csv to make converter
lstsite = []
lstprov = []
lstcode = []
conv = open("sites.full_list.csv", "r")
reader = list(csv.reader(conv))
for x in range(len(reader)):
    line = reader[x]
    site = line[0]
    prov = line[1]
    code = line[2]
    lstsite.append(site)
    lstprov.append(prov)
    lstcode.append(code)

lstcombo = zip(lstsite, lstprov)
codestationdict = dict(zip(lstcode, lstcombo))


def paireCalculator(time, forecast):
    if time == "AM" and forecast == "Today":
        return "1"
    if time == "AM" and forecast == "Tonight":
        return "2"
    if time == "AM" and forecast == "Tomorrow":
        return "3"
    if time == "PM" and (forecast == "Tonight" or forecast == "Today"):
        return "4"
    if time == "PM" and forecast == "Tomorrow":
        return "5"
    else:
        return "-"


templist = ["Site,Province,isueTime,AM_PM,Paire,CASe,CASi,File"]
# file in, add loop for later
for f in os.listdir("a"):
    print(f)
    tree = ET.ElementTree(file="a/" + f)
    root = tree.getroot()

    time = ""
    site = ""
    province = ""
    issuetime = ""
    format24h = ""
    # finds initial informaiton
    for region in root:
        if region.tag == "region":
            ident = codestationdict[region.text]
            print(region.attrib['nameEn'], ident)

            site = ident[0].strip()
            province = ident[1].strip()
        if region.tag == "dateStamp":
            if region[3].attrib['ampm'] == "PM":
                if int(region[3].text) != 12:
                    format24h = int(region[3].text) + 12
                else:
                    format24h = int(region[3].text)
            else:
                format24h = int(region[3].text)
            time = region[3].attrib['ampm']
            print(int(region[0].text), int(region[1].text), int(region[2].text), int(format24h))
            issuetime = datetime.datetime(int(region[0].text), int(region[1].text), int(region[2].text), int(format24h))

    print("-----")
    # find in smoke
    for insmoke in root[4]:
        # if the len is 3, it means that it doesnt contain in smoke exception
        if len(insmoke) is 4:
            print(insmoke[0].attrib['forecastName'])
            case = re.findall("\d", insmoke[3].text)
            print("CASe: " + str(case))
            casi = re.findall("\d", insmoke[2].text)
            print("CASi: " + str(casi))
            a = paireCalculator(time, insmoke[0].attrib['forecastName'])
            print("paire: " + a)

            # for the ["1","0"] CASe, it needs to be together.
            if len(case) is 2:
                towrite = site + "," + province + "," + issuetime.strftime(
                    "%Y/%m/%d %H:00:00") + "," + time + "," + a + "," + case[0] + case[1] + "," + casi[0] + "," + f
                templist.append(towrite)
                print(towrite)
            else:
                towrite1 = site + "," + province + "," + issuetime.strftime(
                    "%Y/%m/%d %H:00:00") + "," + time + "," + a + "," + case[0] + "," + casi[0] + "," + f
                templist.append(towrite1)
                print(towrite1)
    print("-----------------------------------------------------------------------------------")

csvFile = open("out.csv", "w+")
for i in templist:
    csvFile.write(i + "\n")
