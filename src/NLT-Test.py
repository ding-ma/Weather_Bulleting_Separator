import nltk

ss = open("output.txt").read()
tokens = nltk.word_tokenize(ss)
tag = nltk.pos_tag(tokens)
for t in tag:
    print(t[0], t[1])
