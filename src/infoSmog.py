import calendar
import collections
import os
import re
import sys
from datetime import datetime

import pandas as pd

# if the script crashes due to 'ValueError'>: time data '2012 1 1 5.00 AM' does not match format '%Y %m %d %I:%M %p')
# check def fixtime(time):


# part 1 of script, separates the bulletin per day
loc = os.getcwd()

dirs = ["Input", "Output", "FLCN"]
for dir in dirs:
    if not os.path.exists(loc + "/" + dir):
        os.mkdir(loc + "/" + dir)
monthdict = dict((v, k) for k, v in enumerate(calendar.month_name))
print("Select the name of the file you would like to treat and press enter")
for F in os.listdir(loc + "/Input"):
    if not os.path.exists(loc + "/Input"):
        os.mkdir(loc + "/Input")
    print(F)

filein = input()
file = open("Input/" + filein, "r").read()
beginingofdate = re.compile(("AT(\n.*|.*|.*\n.*)\d{4}"))
# LCN41 CWUL (.*\n)*(END)\n\nFLCN41
start = re.compile("FLCN41 CWUL \d{6}( AA.)?")
end = re.compile("END")
templst = []
datelst = []
t = []

def fixtime(time):
    year = time[6]
    month = monthdict[time[5].capitalize()]
    day = time[4]
    time_12h = time[0] + " " + time[1].replace(".", "")
    try:
        yearMonthDay = datetime.strptime(year + " " + str(month) + " " + str(day) + " " + time_12h,
                                         "%Y %m %d %I.%M %p").strftime("%p-%Y%m%d-%H%M")
    except ValueError:
        yearMonthDay = datetime.strptime(year + " " + str(month) + " " + str(day) + " " + time_12h,
                                         "%Y %m %d %I:%M %p").strftime("%p-%Y%m%d-%H%M")
    return yearMonthDay


for y in start.finditer(file):
    yearstr = file[y.start():y.end() + 410]
    for s in beginingofdate.finditer(yearstr):
        fixedTime = fixtime(re.split("\n|\s", yearstr[s.start() + 3:s.end()]))
        t.append(yearstr[s.start() + 3:s.end()])
        templst.append(fixedTime)

startofFile = []
for a, b in zip(start.finditer(file), end.finditer(file)):
    startofFile.append([a.start(), b.end()])

for fileName, filecontent in zip(templst, startofFile):
    f = open("FLCN/" + fileName + ".txt", "w+")
    f.write(file[filecontent[0]:filecontent[1]].replace("SMOG WARNING IN EFFECT.\n", ""))

repeatedFiles = [item for item, count in collections.Counter(t).items() if count > 1]
print("These Files are the Same")
for r in repeatedFiles:
    print(r)

# part 2 of script, does the search and outputs to csv
# regions, this uses regex to find the match
# if more regions are added, make sure the add them to regex_lst
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

#######################

weekdayMatcher = re.compile("(TONIGHT|TODAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)\.\.AIR QUALITY ")
indice = re.compile("GOOD|FAIR|POOR")
daytoWrite = re.compile("(TONIGHT|TODAY|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)")
amendment = re.compile("FLCN41 CWUL \d{6}( AA.)?")
dayofweek = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


# find the value pair, if it is a weekday, it means taht
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


# returns the date into something more usable
def fixdate(yh):
    year = yh[0:4]
    month = yh[4:6]
    Day = yh[6:8]
    hour = yh[8:10]
    minutes = yh[10:]
    return year + "/" + month + "/" + Day, hour + ":" + minutes


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


# begings by writting the start of the file into a list
lstofAmendment = []
for files in os.listdir("FLCN"):
    AM_PM = files[:2]
    f = open("FLCN/" + files).read()
    for amended in amendment.finditer(f):
        lstofAmendment.append(amended.group())

# initiate counters for different loops
i, k = 0, 0
prog = len(lstofAmendment)
df = pd.DataFrame(columns=["Region", "Date", "Heure", "Paire", "Indicateur", "Amendement"])
for files, amd in zip(os.listdir("FLCN"), lstofAmendment):
    AM_PM = files[:2]
    f = open("FLCN/" + files).read()
    k = k + 1
    # progress(k, prog, '')
    print(k / prog)
    # expands regex list
    for reg in regex_lst:
        # uses every regex to find what they need
        for element in reg.finditer(f):
            # i found that 85 character was a good balance, the region then matches with good/poor/fair AQ
            textTomatch = f[element.start():element.end() + 85]
            for day, ind in zip(weekdayMatcher.finditer(textTomatch), indice.finditer(textTomatch)):
                # separate even further for the pair
                for dayWrite in daytoWrite.finditer(day.group()):
                    region = element.group().replace("\n", " ")
                    date = files[:-4].split("-")
                    yearHour = fixdate(date[1] + date[2])
                    Paire = pairValuefinder(dayWrite.group(), AM_PM)
                    Indince = ind.group()
                    # print(files,AM_PM,region, yearHour[0], yearHour[1], Paire, Indince)
                    # checks if it is amanded, add to dataFrame
                    if bool(re.search("AA.", amd)) is True:
                        df.loc[i] = [region, yearHour[0], yearHour[1], Paire, Indince, "YES"]
                    else:
                        df.loc[i] = [region, yearHour[0], yearHour[1], Paire, Indince, "NO"]
                    i = i + 1

# save dataFrame to csv
df.to_csv("Output/treated_" + filein[:-4] + ".csv", index=False, index_label=False)
print("Job Done see -->" + loc + "/output")
# shutil.rmtree(loc + "/FLCN")
