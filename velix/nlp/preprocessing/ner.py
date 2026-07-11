def ner(doc):
    """
    Purpose: Named Entity Recognition
    """
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities