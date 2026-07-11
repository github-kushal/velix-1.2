def dependency_parser(doc):
    """
    Purpose: Extract dependency relations.
    """

    dependencies = []

    for token in doc:
        dependencies.append(
            (
                token.text,
                token.dep_,
                token.head.text
            )
        )

    return dependencies