"""
Dictionary of sentiwordnet translation.
"""
nltk_to_senti = {'VB':'v', 'VBD':'v', 'VBG':'v', # Verbs
                  'VBN':'v', 'VBP':'v', 'VBZ':'v',
                  'NN':'n', 'NNS':'n', # Nouns
                  'NNP':'n', 'NNPS':'n', # Proper nouns
                  'JJ':'a', 'JJR':'a', 'JJS':'a', # Adjectives
                  'RB':'r', 'RBR':'r','RBS':'r', # Adverbs
                  'PRP': 'n', 'WP': 'n', # Pronouns
                  'WRB': 'r'} # wh-adverb
                  # nltk to sentiwordnet labelling.