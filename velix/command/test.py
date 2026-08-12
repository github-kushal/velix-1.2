# Language: Python

# Necessary imports
import spacy
from spacy import displacy

# Load the English language model
# Note: make sure you have 'en_core_web_sm' installed: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_lg")

# Example sentence
sentence = "search for lo-fi music on YouTube"

# Parse the sentence using SpaCy
doc = nlp(sentence)

# Print dependency info (for inspection)
for token in doc:
    print(f"Token: {token.text}, POS: {token.pos_}, Dep: {token.dep_}, Head: {token.head.text}")

# Visualize dependency tree in Jupyter Notebook or similar environment
# You can also save as HTML to view in a browser
displacy.render(doc, style="dep", jupyter=True, options={'distance': 120})

# Optional: save visualization as HTML
html_file = "dependency_tree.html"
html = displacy.render(doc, style="dep", page=True, options={'distance': 120})
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Dependency tree saved as {html_file}")