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
    parent : Tcl notebook object
        Tcl Tk notebook that stores the tab.
    raw : str
        Raw string of input data.
    text: TKinter text box widget
        Text box widget stored inside the tab.
    xdim: int
        Horizontal size of the tab window in pixels.
    ydim: int
        Vertical size of the tab window in pixels.
    tab_name: str
        Name of the tab.
    md : Spacy classifier object
        Word analysis class.


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

        self.highlighted_text_list = {}
        self.text_selected = tk.StringVar()
        # List of all currently highlighted text (currently empty).

    @log.log_function
    def add_text_box(self):
        """
        Add a new text box to the tab.
        """
        self.text = tk.Text(self, height=self.xdim,
                            width=self.ydim, wrap='word',
                            font=('Tempus Sans ITC', 12),
                            undo=True)
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
        """
        Get the start and end index/column positions of the text.
        """
        start_index = str(index)
        end_index = '{}+{}c'.format(start_index, len(text))

        return start_index, end_index

    @log.log_function
    def classify_word_types(self, to_include):
        """
        Classify and highlight specific word types.
        """
        self.raw = self.text.get('1.0', tk.END)
        # Get current text input.

        wc = wd.WordSet(self.raw, self.md_core)
        wc.label_word_types()
        # Label word types.

        flatten = [x for y in to_include for x in y]
        # Get rid of tupples.

        for w, t in list(set(wc.pos)):
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

        repeated_w = {}
        #Record words which are repeated.

        for w in wc.token:
            if w == keyword:
                reg_search = r'\y'+w+r'\y'
                index_pos = self.text.search(reg_search, index_pos, regexp=True,
                                             stopindex='end')
                # Search for text keyword as individual word.
                self.colourise_text(w, 'snow', color, name, index_pos)
                start, index_pos = self.index_start_and_end(index_pos, w)
                # Set index to begin highlighting at the end of the matched
                # word.

                # Number of occurences of w in keys:
                if w in repeated_w.keys():
                    # Subsequent repeats.
                    repeated_w[w] += 1
                    w = w + str(repeated_w[w])
                    # Rename w to include occurences.
                elif w in self.highlighted_text_list.keys():
                    repeated_w[w] = 2
                    # First repeat.
                    w = w + str(repeated_w[w])
                    # Rename w to include occurences.

                self.highlighted_text_list[w] = (start, index_pos)
                # Add word and position bounds to dictionary.

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

        return highlighted_by_cursor

    @log.log_function
    def similarity_of_highlighted_texts(self):
        """
        Get the similarities of two sections of highlighted text.
        """

        wc = wd.WordSet(self.raw, self.md_core)

        self.text.config(cursor='@icons//highlighter_tip.cur')
        # Change cursor for highlights.

        if self.text.tag_ranges(tk.SEL):
            h1 = self.tag_highlighted_text(colour='blue', tag_name='h1')
        else:
            self.wait_variable(self.text_selected)
            h1 = self.tag_highlighted_text(colour='blue', tag_name='h1')

        self.wait_variable(self.text_selected)
        # Wait for next highlight.
        h2 = self.tag_highlighted_text(colour='red', tag_name='h2')

        self.text.config(cursor='arrow')
        # Return cursor to arrow.

        sim, color = wc.spacy_sim(h1, h2)

        self.text_selected = tk.StringVar()
        # Reset the text selection variable.

        return sim

    @log.log_function
    def get_highlighted_word_by_click(self, event):
        """
        Turn highlighted words into buttons.
        """
        cursor_position = self.text.index(tk.INSERT)
        # Get cursor position (as user clicking gives this location).

        for t, v in zip(self.highlighted_text_list.keys(),
                        self.highlighted_text_list.values()):

            start_f = v[0].split('.')
            # Starting index.
            to_add = v[1].split('+')
            to_add = to_add[1]
            to_add = to_add[:-1]
            # Number of characters to add.
            end_f = str(int(start_f[1])+int(to_add))
            # Convert end string from character addition to coordinate.
            cursor_f = cursor_position.split('.')
            # Change the word end and cursor position into floats.

            if all([int(cursor_f[0]) == int(start_f[0]),
                    int(cursor_f[1]) < int(end_f),
                    int(cursor_f[1]) > int(start_f[1])]):
                # Select if cursor position falls between the start and end
                # of the word.
                self.colourise_text(t, 'snow', 'red', t, v[0])
                # Add a highlight.
                self.text_selected.set(t)

    @log.log_function
    def bind_to_selection(self):
        """bind_to_selection
        Unbind left button press from previous
        binding and rebind it to capture sentences.
        """

        hb = self.text.bind("<Button 1>", self.get_highlighted_word_by_click)

        self.text.config(cursor='@icons//hand_select.cur')
        # Change cursor to click.

        self.wait_variable(self.text_selected)
        # Wait for next highlight.

        self.similarity_to_all_highlighted()

        self.text.config(cursor='arrow')
        # Return cursor to arrow.

        self.text.unbind("<Button 1>", funcid = hb)
        self.text_selected = tk.StringVar()
        # Reset selected to empty.

    @log.log_function
    def similarity_to_all_highlighted(self):
        """
        Get similarity of the highlighted word to all other
        highlighted words.
        """

        wc = wd.WordSet(self.raw, self.md_core)

        for k, v in zip(self.highlighted_text_list.keys(),
                        self.highlighted_text_list.values()):
            # Check to see which sentence is being highlighted.

            s = ''.join(['' if i.isdigit() else i for i in k])
            # Remove numeric elements for words appearing twice.
            sim, color = wc.spacy_sim(self.text_selected.get(), s)

            self.colourise_text(s, 'snow', color, s, v[0])
            # Highlight text.

    @log.log_function
    def sentiment_analysis(self):
        """
        Highlight positive and negative sentiment for all words or
        all highlighted words.
        """

        wc = wd.WordSet(self.raw, self.md_core)

        if self.highlighted_text_list:
            # Highlight only selected words.

            for s, v in zip(self.highlighted_text_list.keys(),
                            self.highlighted_text_list.values()):

                pos, neg, obj, color = wc.sentiment(s)
                self.colourise_text(s, 'snow', color, s, v[0])
                # Highlight text.
        else:
            # Highlight all words.
            pos, neg, obj, color = wc.sentiment_all()

            for c, k in zip(color, wc.token):
                self.highlight_words(k, wc, color=c, name='highlight')



