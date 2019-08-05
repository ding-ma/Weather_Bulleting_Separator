import csv
import os
import re
import xml.etree.ElementTree as ET

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
        return "---"


templist = ["Site,Province,Paire,CASe"]
# file in, add loop for later
for f in os.listdir("process"):
    print(f)
    tree = ET.ElementTree(file="process/" + f)
    root = tree.getroot()

    time = ""
    site = ""
    province = ""
    # finds initial informaiton
    for region in root:
        if region.tag == "region":
            ident = codestationdict[region.text]
            print(region.attrib['nameEn'], ident)

            site = ident[0].strip()
            province = ident[1].strip()
        if region.tag == "dateStamp":
            print(region[0].text, "month:" + region[1].text, "day:" + region[2].text,
                  region[3].text + region[3].attrib['ampm'])
            time = region[3].attrib['ampm']

    print("-----")
    # find in smoke
    for insmoke in root[4]:
        print(insmoke[0].attrib['forecastName'])
        case = re.findall("\d", insmoke[2].text)
        print("CASe: " + str(case))
        a = paireCalculator(time, insmoke[0].attrib['forecastName'])
        print(a)
        if len(case) is 2:
            templist.append(site + "," + province + "," + a + "," + case[0] + case[1])
            print(site + "," + province + "," + a + "," + case[0] + case[1])
        else:
            templist.append(site + "," + province + "," + a + "," + case[0])
            print(site + "," + province + "," + a + "," + case[0])
    print("-----------------------------------------------------------------------------------")

csvFile = open("out.csv", "w+")
for i in templist:
    csvFile.write(i + "\n")
