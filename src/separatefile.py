import calendar
import collections
import re
from datetime import datetime

monthdict = dict((v, k) for k, v in enumerate(calendar.month_name))
file = open("Input/2015.txt", "r").read()
beginingofdate = re.compile("AT (\n|.*)(\n)?\d{4}")
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
    yearMonthDay = datetime.strptime(year + " " + str(month) + " " + str(day) + " " + time_12h,
                                     "%Y %m %d %I.%M %p").strftime("%p-%Y%m%d-%H%M")
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
