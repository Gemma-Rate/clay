"""
Classes for analysing prose itself.
"""
import nltk
from nltk.corpus import wordnet as wn
import re
import log

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
        self.token = self.word_token(text, no_punctuation=None, lower=None)
        # Keeps in punctuation and upper cases.
        self.processed = self.word_token(text)
        self.pos = None
        self.word_colours = {'VB':'blue', 'VBD':'blue', 'VBG':'blue',
                             'VBN':'blue', 'VBP':'blue', 'VBZ':'blue',
                             'NN':'red', 'NNS':'red', 'NNP':'red4',
                             'NNPS':'red4', 'JJ':'green', 'JJR':'green',
                             'JJS':'green'}


    def label_word_types(self):
        """
        Parameters
        ----------
        tagger : function
            Pos tagger to use.

        Returns
        ----------
        """

        pos_text = nltk.pos_tag(self.processed)

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

    @log.log_function
    def word_token(self, data, no_punctuation=True, lower=True):

        """
        Strips out the punctuation and tokenises words in the input string
        data.

        Parameters
        -----------
        data : string
        String containing data to be tokenised.

        Returns
        -------
        datatoken : list
        List of tokenised data.

        """

        if no_punctuation:
            data = re.sub(r"[^\w\s]", ' ', data)
            # Remove punctuation.
        if lower:
            datatoken = nltk.word_tokenize(data.lower())
        else:
            datatoken = nltk.word_tokenize(data)

        return datatoken

