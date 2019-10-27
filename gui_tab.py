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

    def __init__(self, parent, xdim, ydim, tab_name, md):
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

        self.md_core = md
        # Classifier from Spacy, loaded in gui_windows.

        self.higlighted_text_list =[]
        self.text_selected = tk.StringVar()
        # List of all currently highlighted text (currently empty).

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

        self.text.bind('<B1-Motion><ButtonRelease-1>',
                       self.capture_highlighted_text)
        # Set capture_highlighted_text as selected by the text box.
        self.text.bind('<KeyRelease>', self.update_raw)
        # Set update for when new text is written.

    @log.log_function
    def update_raw(self, event):
        """
        Update the raw data, based on input from user.
        """
        self.raw = self.text.get('1.0', tk.END)


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
        # Add highlight to text.

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
    def highlight_word_types(self, to_include):
        """
        Highlight specific word types.
        """
        self.raw = self.text.get('1.0', tk.END)
        # Get current text input.
        wc = wd.WordSet(self.raw, self.md_core)
        # Make a class of the data.
        wc.label_word_types()
        # Label word types.

        flatten = [x for y in to_include for x in y]
        # Get rid of tupples.

        for w, t in wc.pos:
            if t in flatten:
                try:
                    colour = wc.word_colours[t]
                    self.highlight_words(w, wc, name=t, color=colour)
                except KeyError:
                    pass
            else:
                pass
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
        for w in wc.token:
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
    def capture_highlighted_text(self, event):
        """
        Capture text that is highlighted.
        """
        highlighted_by_cursor = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_selected.set(highlighted_by_cursor)


    @log.log_function
    def tag_highlighted_text(self, colour='blue', tag_name='highlight'):
        """
        Tag the text from capture_highlighted_text.
        """

        highlighted_by_cursor = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        # Get text currently highlighted by cursor.
        start = self.text.search(highlighted_by_cursor, '1.0',
                                     stopindex="end", count=1)
        # Start point of text.
        end = self.text.index(tk.INSERT)

        self.text.tag_config(tag_name, foreground='snow', background=colour,
                             font=('Tempus Sans ITC', 12))
        self.text.tag_add(tag_name, start, end)
        # Highlight the text in colour.

        #self.text.tag_remove(tk.SEL_FIRST, tk.SEL_LAST)
        # Deselect the text.

        return highlighted_by_cursor

    @log.log_function
    def similarity_of_highlighted_texts(self):
        """
        Get the similarities of two sections of highlighted text.
        """

        wc = wd.WordSet(self.raw, self.md_core)

        if self.text.tag_ranges(tk.SEL):
            h1 = self.tag_highlighted_text(colour='blue', tag_name='h1')
        else:
            self.wait_variable(self.text_selected)
            h1 = self.tag_highlighted_text(colour='blue', tag_name='h1')

        self.wait_variable(self.text_selected)
        # Wait for next highlight.
        h2 = self.tag_highlighted_text(colour='red', tag_name='h2')

        sim = wc.spacy_sim(h1, h2)

        return sim

    @log.log_function
    def similarity_to_all_sentences(self, selected_sentence):
        """
        Get similarity of the highlighted sentence to all other sentences.
        """
        index = '1.0'
        wc = wd.WordSet(self.raw, self.md_core)

        #for s in wc.sentences:
            # Check to see which sentence is being highlighted.


        #self.index_start_and_end(index, text)


        pass

