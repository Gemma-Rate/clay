"""
Classes for analysing prose itself.
"""
import nltk
from nltk.corpus import wordnet as wn
import key_functions as kf
import gui_windows as gu

# Highlighting.
# Nearby word similarity.
# Sentence simliarity (repetition).
# Word recommendation.
    # Blurring etc.

class WordSet(object):

    """
    Words object class.

    Public attributes
    -----------------
    raw : str
        Raw string of input data.
    processed : list
        List of tokenised words.

    Class methods
    -----------------
    word_token : static class method
        Strips out punctuation and tokenises words in the input string.
    olist : class method
        Opens the created hdf5 file and lists training file names.

    """

    def __init__(self, text):
        self.raw = text
        self.token = kf.word_token(text, no_punctuation=None, lower=None)
        # Keeps in punctuation and upper cases.
        self.processed = kf.word_token(text)
        self.pos = None


    def label_word_types(self, tagger):
        """
        Parameters
        ----------
        tagger : function
            Pos tagger to use.

        Returns
        ----------
        """

        pos_text = tagger(self.processed)

        self.pos = pos_text


    def txt_percent(self):
        """
        Gets percentage of text with different labels.

        Parameters
        ----------


        Returns
        ----------
        """
        pass

