"""
Classes for analysing prose itself.
"""
import log
import highlight_dictionary as hd
import textblob as tx
from nltk.corpus import wordnet as wn
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
        self.blob = tx.TextBlob(text)
        self.token = self.blob.words
        # Keeps in punctuation and upper cases.
        self.sentences = self.blob.sentences
        self.pos = self.blob.tags

        self.word_colours = hd.highlight_nltk
        self.md_core = md

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
        try:
            s = wn.synsets(words_in)
            # Create wordnet object.

            s_set = swn.senti_synset(s[0].name())
            # Take first element as most common meaning.
            pos, neg = s_set.pos_score(), s_set.neg_score()
            obj = s_set.obj_score()

            r, g, b = int(255*neg), int(255*pos), int(255*obj)
            color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        except:
            pos, neg, obj = 0, 0, 0
            color = "#{:02x}{:02x}{:02x}".format(255, 255, 255)

        return pos, neg, obj, color

    @log.profiler
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
