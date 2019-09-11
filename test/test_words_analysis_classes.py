import unittest
import gui_windows as gu
import words_analysis_classes as wc
import tkinter as tk
import key_functions as kf
import log

class MyTestCase(unittest.TestCase):

    def test_wordcolour(self):
        """Test highlighting words in a given colour."""
        log.log_setup()
        # Start logging.

        text = 'I was about to go shopping, but it was raining. So I decided to stay at home instead.'
        app = gu.MainWindow(None, text)
        app.title('Prose analysis')
        app.grid_config()

        ws = wc.WordSet(text)
        app.highlight_words('was', ws)
        app.mainloop()

    def test_label_word_types(self):
        """Test type tagger."""
        log.log_setup()
        # Start logging.

        text = 'I was about to go shopping, but it was raining. So I decided to stay at home instead.'
        app = gu.MainWindow(None, text)
        app.title('Prose analysis')
        app.grid_config()

        ws = wc.WordSet(text)
        app.highlight_words('was', ws)
        app.mainloop()


if __name__ == '__main__':
    unittest.main()
