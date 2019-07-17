inputfile = open("bulletin.txt").read()

lines = inputfile.split("\n")
containsSmoke = "IN SMOKE."
containsStars = "*** "
containsEnd = "END"

smokelist = []
starlst = []
emptylist = []
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

    for a in lines[start:end]:
        f.write(a)
        f.write("\n")
    for b in lines[lowerSpace:upperSpace+1]:
        f.write(b)
        f.write("\n")
    f.write("\n")