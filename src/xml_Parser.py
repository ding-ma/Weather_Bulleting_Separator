import csv
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

# file in, add loop for later
tree = ET.ElementTree(file="example.xml")
root = tree.getroot()

# finds initial informaiton
for region in root:
    if region.tag == "region":
        print(region.attrib['nameEn'], codestationdict[region.text])
    if region.tag == "dateStamp":
        print(region[0].text, "month:" + region[1].text, "day:" + region[2].text,
              region[3].text + region[3].attrib['ampm'])

print("-----")
# find in smoke
for insmoke in root[4]:
    print(insmoke[0].attrib['forecastName'])
    print("CASe: " + re.findall("\d", insmoke[2].text)[0])
