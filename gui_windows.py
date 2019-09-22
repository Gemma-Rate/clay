"""
GUI windows class
"""

import tkinter as tk
import tkinter.ttk
import tkinter.filedialog
import log
import gui_tab as tb

class MainWindow(tk.Tk):
    """
    Overview class for total window.

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
        self.raw = text
        # Raw entry text (not modified).
        self.tag_colors = {''}

        self.current_tab = None
        self.tab_no = None
        # Empty attributes to fill later.

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

        #Make a frame:
        self.frame.grid(row=0, sticky="ew")

        # Paned window split:
        self.panes = tk.PanedWindow(self.master, orient ='horizontal')
        self.panes.grid(row=0, sticky="ew")

        # Make notebook for tabs:

        self.parent_tabs = tk.ttk.Notebook(self.panes)
        self.parent_tabs.bind('<<NotebookTabChanged>>', self.select_tab_type)
        # Bind tab frame so that changing notebook tab triggers tab text
        # selection.
        self.panes.add(self.parent_tabs)

        # Add tab:
        self.new_tab()
        # Make a text box with this tab:

        self.add_tab_button()

        self.update()
        # Update based on events.

    @log.log_function
    def save_file(self, tab):
        """
        Save the text in the main grid.
        """
        data = tab.text.get("1.0", 'end-1c')
        file = tk.filedialog.asksaveasfilename(defaultextension='.txt',
                                               filetypes=(("txt files",
                                                           "*.txt"),
                                                          ("all files",
                                                           "*.*")),
                                               title="Save file")

        with open(file, 'w') as f:
            f.write(data)

        self.parent_tabs.tab(tab, text=file)
        # Change tab name to saved file name.

    @log.log_function
    def open_file(self, tab):
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
            tab.text.delete("1.0", tk.END)
            # Remove old text.
            tab.text.insert(tk.INSERT, data)
            # Insert the text from the file.

        self.parent_tabs.tab(tab, text=file)
        # Change tab name to loaded file name.

    @log.log_function
    def new_file(self, tab):
        """
        Check if the current file should be saved,
        then create a new file.
        """
        self.save_file(tab)
        tab.text.delete("1.0", tk.END)

        default_tab_name = 'Doc ' + str(len(self.parent_tabs.tabs()))
        self.parent_tabs.tab(tab, text=default_tab_name)
        # Change tab label back to default.

    @log.log_function
    def menu(self):
        """
        Add top bar menu ribbon.
        """

        self.menu = tk.Menu(self.frame)
        # Main menu ribbon.

        """Menu for files:"""
        self.file_menu = tk.Menu(self.menu)

        self.file_menu.add_command(label="New", command=lambda : self.new_file(self.current_tab))
        self.file_menu.add_command(label="Open", command=lambda : self.open_file(self.current_tab))
        self.file_menu.add_command(label="Save", command=lambda : self.save_file(self.current_tab))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=self.menu)


    @log.log_function
    def new_tab(self, event=None):
        """
        Add a new text box tab.
        """
        default_tab_name = 'Doc '+str(len(self.parent_tabs.tabs()))

        tab_w_box = tb.TabTextBox(self.parent_tabs, self.raw, self.master_height,
                                  self.master_width, default_tab_name)
        # Internal container class.
        self.parent_tabs.grid(sticky='EW')
        self.parent_tabs.add(tab_w_box, text=tab_w_box.tab_name)
        tab_w_box.add_text_box()

        return tab_w_box

    @log.log_function
    def auto_update(self):
        """
        Auto update the main word grid.
        """
        pass

    @log.log_function
    def select_tab_type(self, event):
        """
        Select tab class based on currently selected tab.
        """
        current_tab_name = self.parent_tabs.select()
        self.current_tab = self.parent_tabs.nametowidget(current_tab_name)
        # Get current tab (for open/closing functions).

    @log.log_function
    def add_tab_button(self):
        """
        Button for generating new tabs.
        """
        tab_host = tk.ttk.Button(self.panes, text='+')
        tab_host.grid(row=0, column=1)
        # Add a button.
        tab_host.bind('<Button-1>', self.new_tab)
        # Create new tab when pressing the new tab button.

