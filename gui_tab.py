"""
GUI class for tab objects.
"""

import tkinter as tk
import words_analysis_classes as wd
import log

class TabTextBox(tk.Frame):
    """
    Container class for tab with a text box attached.

    Public attributes
    -----------------
    raw : str
        Raw string of input data.
    processed : list
        List of tokenised words.

    Class methods
    -----------------

    """

    def __init__(self, parent, xdim, ydim, tab_name):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.text = None
        self.raw = None
        # Raw entry text (not modified).

        self.tag_colors = {''}
        self.xdim = xdim - 20
        # Full x dimension of the tab widget area.
        self.ydim = ydim - 10
        # Full y dimension of the tab widget area.
        self.tab_name = tab_name

        # Frame to store things in.

    @log.log_function
    def add_text_box(self):
        """
        Add a new text box to the tab.
        """
        self.text = tk.Text(self, height=self.xdim,
                            width=self.ydim, wrap='word',
                            font=('Tempus Sans ITC', 12))
        # Make a text object.

        self.text.grid(column=0, row=0, sticky='EW')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #self.text.insert(tk.END, self.raw)
        # Add text.
        self.scrollbar()
        # Add the scrollbar.

    @log.log_function
    def colourise_text(self, text, fgcolour, bgcolour, name, index):
        """
        Make text a different colour.

        Parameters
        -----------
        text : string
            String containing text for colour change.
        fgcolor : tuple
            Foreground colour of text.
        bgcolor : tuple
            Background colour of text.
        name : string
            Tag name to assign, to avoid overwriting other colours.

        """
        self.text.tag_config(name, foreground=fgcolour, background=bgcolour,
                             font=('Tempus Sans ITC', 12))
        # Set tagging configuration.


        start, end = self.index_start_and_end(index, text)
        self.text.tag_add(name, start, end)
        #self.text.insert(tk.END, text, name)
        # Add highlight to element of text.

    @log.log_function
    def index_start_and_end(self, index, text):

        start_index = str(index)
        index_split = start_index.split('.')
        end_index = index_split[0]+'.'+str(int(index_split[1])+len(text))

        return start_index, end_index

    @log.log_function
    def insert_spaces(self):
        """
        Insert space into a text block.
        """
        position = self.text.index(tk.INSERT)
        last_insert = self.text.get('1.0', position)[-1]
        punctuation = ['.', ',', ';', ':']

        if last_insert in punctuation:
            # Take out the space before punctuation.
            delete_location = position+'-2c'
            self.text.delete(delete_location)

        self.text.insert(tk.END, ' ')

    @log.log_function
    def highlight_word_types(self):
        """
        Highlight specific word types.
        """
        self.raw = self.text.get('1.0', tk.END)
        # Get current text input.
        wc = wd.WordSet(self.raw)
        # Make a class of the data.
        wc.label_word_types()
        #self.text.delete("1.0", tk.END)
        # Delete text in box.
        self.highlight_words('the', wc, name='the')
        self.highlight_words('toilet', wc, name='toilet', color='green')
        # Use the data save in the WordSet class to input the same
        # text, but highlighted.

    @log.log_function
    def highlight_words(self, keyword, wc, color='blue', name='highlight'):
        """
        Highlight specific words.

        Parameters
        -----------
        text : string
            String containing text for colour change.
        keyword : string
            String containing word to highlight.
        wc : WordSet object
            Class of all words in the text box.
        color : tuple
            String of containing colour.
        """
        # Store indices of punctuation marks to delete extra spaces.
        index_pos = '1.0'
        for i,w in enumerate(wc.token):
            if w == keyword:
                index_pos = self.text.search(w, index_pos, stopindex="end")
                self.colourise_text(w, 'snow', color, name, index_pos)

                start, index_pos = self.index_start_and_end(index_pos, w)
                # Set index to begin highlighting at the end of the matched
                # word.

    @log.log_function
    def scrollbar(self):
        """
        Add a scrollbar to the word window.
        """

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=0, sticky='N'+'S'+'W')
        # Add scrollbar on the right.

        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)


    @log.log_function
    def capture_text(self):
        """
        Capture text entered into the tab text box.
        """
        #<Key>
        pass
