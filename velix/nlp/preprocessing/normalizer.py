import re 
import unicodedata
import contractions


class TextPreProcessor:
    def __init__(self, text:str):
        """
        Purpose: Pre Process the text for intext classification and entity extraction. 
        """
        self.text = text
        # self.normalizer()
        # self.unicode_normalize()
        # self.expand_contractions()

    def normalizer(self):
        """r
        Purpose: Clean and normalize raw text.
        """

        PUNCT_REGEX = re.compile(r"[^\w\s.%:/'-]")
        SPACE_REGEX = re.compile(r"\s+")

        self.text = PUNCT_REGEX.sub("", self.text)
        self.text = SPACE_REGEX.sub(" ", self.text)
        self.text = self.text.lower()
        # print(f"normalized : {self.text}")
        return self.text
        # print(f"normalized : {self.text}")

    def unicode_normalize(self, form="NFKC"):
        try:
            self.text = unicodedata.normalize(form, self.text)
            # print(f"unicode_normalized : {self.text}")
            return self.text
        except ValueError as e:
            raise ValueError(f"Invalid normalization form: {form}") from e

    def expand_contractions(self):
        """
        Purpose: 
        """
        try:
            txt = self.text
            self.text = contractions.fix(txt)
            # print(f"expand_contractions : {self.text}")
            return self.text
        except Exception as e:
            raise e
        
    def preprocess(self):
        self.unicode_normalize()
        self.expand_contractions()
        self.normalizer()
        print(self.text)
        return self.text

# txt="I Can’t Believe he won’t be able to Make it to the Party Tonight."
# tpp = TextPreProcessor(txt)
# tpp.preprocess()
# tpp = tpp.normalizer()
# print(tpp)
