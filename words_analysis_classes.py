"""
Classes for analysing prose itself.
"""
import nltk
import re
import log
import highlight_dictionary as hd
from nltk.corpus import sentiwordnet as swn

# Highlighting.
# Content similarity.
# Syntatical/lexical simliarity (repetition) - use Jaccard coefficient.
# Sentiment analysis.
#
# Word recommendation.
    # Blurring etc.
# Named-entity recognition

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

    def __init__(self, text, md):
        self.raw = text
        self.token = self.word_token(text, no_punctuation=None, lower=None)
        # Keeps in punctuation and upper cases.
        self.processed = self.word_token(text)
        self.sentences = nltk.sent_tokenize(text)
        self.pos = None
        self.word_colours = hd.highlight_nltk
        self.md_core = md


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
    def word_token(self, data, no_punctuation=True, lower=False):

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

    @log.log_function
    def spacy_sim(self, s1, s2):
        """
        Get similarity between vectors.
        """
        s1, s2 = self.md_core(s1), self.md_core(s2)
        sim = s1.similarity(s2)

        return sim

    @log.log_function
    def sentiment(self, words_in):
        """
        Positive and negative sentiment polarity for selected word.
        """
        s_set = swn.senti_synset(words_in)
        pos, neg = s_set.pos_score(), s_set.neg_score()
        obj = s_set.obj_score()

        return pos, neg, obj

    @log.log_function
    def wordnet_similar(self, k=9):
        """
        Display similar words, as obtained from wordnet.

        Parameters
        -----------
        k : string
        Number of nearest words to be displayed.

        Returns
        -------
        datatoken : list
        List of tokenised data.

        """
        pass
