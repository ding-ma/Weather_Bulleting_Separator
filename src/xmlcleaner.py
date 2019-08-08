import os
import re

a = re.compile("-.-.-.-.-.-.-.-.-.-.-.-.-")
templst = []
for file in os.listdir("process"):
    f = open("process/" + file, "r")
    fread = f.read()
    for b in a.finditer(fread):
        fout = open("a/" + file, "w+")
        fout.write(fread[:b.start()])
