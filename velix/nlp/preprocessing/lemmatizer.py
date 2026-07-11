def lemmatizer(doc):

    lemma = [token.lemma_ for token in doc]

    print(f"Lemmatized: {lemma}")