import re

file = open("bulletin.txt", "r").read().strip()
splitter = re.split(r'[\n\t\s]|(\.\.)', file)
lst = []

for p, i in enumerate(splitter):
    print(p)
    if i is None:
        splitter.index(i)
        print(splitter.index(i))
# riskList = []
# riskPattern = re.compile("RISK EXCEPT")
# for risk in riskPattern.finditer(file):
#     riskList.append(risk.start())
#
# starlst = []
# datePattern = re.compile("\*\*\* ")
# for star in datePattern.finditer(file):
#     starlst.append(star.start())
#
# for r, d in zip(riskList, starlst):
#     # print(file[d:d+27])
#     riskStr = file[r:r + 37]
#     # print(re.findall(r'\d+', riskStr)[0])
