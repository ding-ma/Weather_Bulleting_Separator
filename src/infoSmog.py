import os
import re
import time

import pandas as pd

s = time.time()
# regions
reg_gatineau = re.compile("GATINEAU\.")
reg_GMA = re.compile(
    "METRO MONTREAL - LAVAL\nVAUDREUIL - SOULANGES - HUNTINGDON\nRICHELIEU VALLEY - SAINT-HYACINTHE\nLACHUTE - SAINT-JEROME\nLANAUDIERE\.")
reg_laurent = re.compile("LAURENTIANS\.")
reg_drum = re.compile("DRUMMONDVILLE - BOIS-FRANCS\.")
reg_maur = re.compile("MAURICIE\.")
reg_town = re.compile("EASTERN TOWNSHIPS\.")
reg_GQA = re.compile("QUEBEC\nMONTMAGNY - L'ISLET\nBEAUCE\.")
reg_abit = re.compile("ABITIBI\.")
reg_temis = re.compile("TEMISCAMINGUE\.")
reg_LSJ = re.compile("LAC-SAINT-JEAN\.")
reg_sag = re.compile("SAGUENAY\.")
reg_riv = re.compile("KAMOURASKA - RIVIERE-DU-LOUP - TROIS-PISTOLES\nTEMISCOUATA\.")
reg_montLaur = re.compile("MONT-LAURIER\.")
reg_latuq = re.compile("LA TUQUE\.")
reg_upperGat = re.compile("UPPER GATINEAU - LIEVRE - PAPINEAU\.")

regex_lst = [reg_gatineau, reg_GMA, reg_laurent, reg_drum, reg_maur, reg_town, reg_GQA, reg_abit, reg_temis, reg_LSJ,
             reg_sag, reg_riv, reg_montLaur, reg_latuq, reg_upperGat]

weekdayMatcher = re.compile("(TONIGHT|TODAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\.\.AIR QUALITY ")
indice = re.compile("GOOD|FAIR|POOR")
daytoWrite = re.compile("(TONIGHT|TODAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)")

dayofweek = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def pairValuefinder(forecast, ampm):
    if ampm == "AM" and forecast == "TODAY":
        return "1"
    if ampm == "AM" and forecast == "TONIGHT":
        return "2"
    if ampm == "AM" and forecast in dayofweek:
        return "3"
    if ampm == "PM" and (forecast == "TONIGHT" or forecast == "TODAY"):
        return "4"
    if ampm == "PM" and forecast in dayofweek:
        return "5"


df = pd.DataFrame(columns=["Region", "Date", "Paire", "Indince?"])

i = 0
for files in os.listdir("FLCN"):
    AM_PM = files[:2]
    f = open("FLCN/" + files).read()
    for reg in regex_lst:
        for element in reg.finditer(f):
            textTomatch = f[element.start():element.end() + 85]
            for day, ind in zip(weekdayMatcher.finditer(textTomatch), indice.finditer(textTomatch)):
                for dayWrite in daytoWrite.finditer(day.group()):
                    region = element.group().replace("\n", " ")
                    date = files
                    Paire = pairValuefinder(dayWrite.group(), AM_PM)
                    Indince = ind.group()
                    print(i)
                    df.loc[i] = [region, date, Paire, Indince]
                    i = i + 1

print(df)
df.to_csv("aaaaaaaaaaaaaaaaaaaaaa.csv")
e = time.time()
print(e - s)
