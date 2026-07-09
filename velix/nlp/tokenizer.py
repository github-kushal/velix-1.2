def tokenizer(doc):

    tokens = [token.text for token in doc]

    return tokens

# txt = "I cant believe he wont be able to make it to the party tonight."
# ttp = TextPreProcessor(txt)
# print(dir(ttp))
# tokenizer(ttp.text)