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
        print(data)

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
        Get similarity between vectors and highlight colour.
        """
        s1, s2 = self.md_core(s1), self.md_core(s2)
        sim = s1.similarity(s2)

        r, g, b = int(17 / 10), 255, 255
        g, b = int((abs(sim) * g)), int((abs(sim) * b))
        color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        # Colour or highlight, based on similarity.

        return sim, color

    @log.log_function
    def sentiment(self, words_in):
        """
        Positive and negative sentiment polarity for selected word.
        """
        s_set = swn.senti_synset(words_in)
        pos, neg = s_set.pos_score(), s_set.neg_score()
        obj = s_set.obj_score()

        r, g, b = 255*neg, 255*pos, 255*obj
        color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return pos, neg, obj, color

    @log.log_function
    def sentiment_all(self):
        """
        Positive and negative sentiment polarity for selected word.
        """
        pos_list, neg_list, obj_list, color_list = [], [], [], []

        for s in self.token:
            pos, neg, obj, color = self.sentiment(s)

            pos_list.append(pos), neg_list.append(neg)
            obj_list.append(obj), color_list.append(color)

        return pos_list, neg_list, obj_list, color_list

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
