def tokenizer(doc):

    return [token.text for token in doc]

    

# txt = "I cant believe he wont be able to make it to the party tonight."
# ttp = TextPreProcessor(txt)
# print(dir(ttp))
# tokenizer(ttp.text)