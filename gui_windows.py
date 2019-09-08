"""
GUI windows class
"""

import tkinter as tk
import tkinter.filedialog
import log

class TextWindow(tk.Tk):
    """
    Class for windows displaying static text.

    Public attributes
    -----------------
    raw : str
        Raw string of input data.
    processed : list
        List of tokenised words.

    Class methods
    -----------------


    """

    def __init__(self, parent, text):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.text = text
        self.raw = text
        # Raw entry text (not modified).
        self.tag_colors = {''}


    @log.log_function
    def grid_config(self):
        """
        Set up a text object widget in the grid.
        """
        self.master_height = 50
        self.master_width = 100

        self.grid()
        # Set grid.

        self.frame = tk.Frame(self.master, height=self.master_height,
                              width=self.master_width, pady=5)
        #Make a frame around the text box.
        self.frame.grid(row=0, sticky="ew")
        self.text = tk.Text(self.frame, height=self.master_height-10,
                            width=self.master_width-10, wrap='word')
        self.text.grid(column=0, row=0, sticky='EW')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.update()
        # Update based on events.


    @log.log_function
    def colourise_text(self, text, fgcolour, bgcolour, name):
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
                            font=('Tempus Sans ITC', 12, 'bold'))
        # Set tagging configuration.
        self.text.insert(tk.END, text, name)
        # Add highlight to element of text.

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
    def highlight_words(self, keyword, wc, color='blue'):
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
        punctuation = []
        # Store indices of punctuation marks to delete extra spaces.
        for i,w in enumerate(wc.token):
            if w == keyword:
                self.colourise_text(w, 'snow', 'blue', 'highlight')
                self.insert_spaces()
            else:
                self.colourise_text(w, 'black', 'snow', 'general')
                self.insert_spaces()

    @log.log_function
    def scrollbar(self):
        """
        Add a scrollbar to the word window.
        """

        scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=0, sticky='N'+'S'+'W')
        # Add scrollbar on the right.

        self.text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text.yview)

    @log.log_function
    def save_file(self):
        """
        Save the text in the main grid.
        """
        data = self.text.get("1.0", 'end-1c')
        file = tk.filedialog.asksaveasfilename(defaultextension='.txt',
                                               filetypes=(("txt files",
                                                           "*.txt"),
                                                          ("all files",
                                                           "*.*")),
                                               title="Save file")

        with open(file, 'w') as f:
            f.write(data)

    @log.log_function
    def open_file(self):
        """
        Open the text in the main grid.
        """

        file = tk.filedialog.askopenfilename(filetypes=(("txt files",
                                                           "*.txt"),
                                                          ("all files",
                                                           "*.*")),
                                               title="Open file")

        with open(file, 'r') as f:
            data = f.read()
            print(data)
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.INSERT, data)


    @log.log_function
    def menu(self):
        """
        Add top bar menu ribbon.
        """

        self.menu = tk.Menu(self.frame)
        # Main menu ribbon.

        """Menu for files:"""
        self.file_menu = tk.Menu(self.menu)

        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=self.menu)

    @log.log_function
    def auto_update(self):
        """
        Auto update the main word grid.
        """
        pass



