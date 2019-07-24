import nltk

ss = """At eight o'clock on Thursday morning Arthur didn't feel very good."""
tokens = nltk.word_tokenize(ss)
tag = nltk.pos_tag(tokens)
print(tag)
