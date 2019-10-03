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

        """Make frames:"""
        self.menu_frame = tk.Frame(self.master, height=self.master_height,
                              width=self.master_width)
        self.menu_frame.grid(row=0, sticky="ew")

        """Paned window split:"""
        self.panes = tk.PanedWindow(self.master, orient ='horizontal')
        self.panes.grid(row=0, sticky="ew")

        """Make notebook for tabs:"""
        self.parent_tabs = tk.ttk.Notebook(self.panes)
        self.parent_tabs.bind('<<NotebookTabChanged>>', self.select_tab_type)
        # Bind tab frame so that changing notebook tab triggers tab text
        # selection.
        self.panes.add(self.parent_tabs)
        self.parent_tabs.grid(sticky='EW')

        # Add tab:
        self.new_tab()
        # Make a text box with this tab.
        self.add_tab_button()
        # Button to add new tabs.
        self.parent_tabs.enable_traversal()
        # Allow tab switching via keyboard.

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
        self.menu = tk.Menu(self.menu_frame)
        # Main menu ribbon.

        """Menu for files:"""
        self.file_menu = tk.Menu(self.menu)

        self.file_menu.add_command(label="New", command=lambda : self.new_file(self.current_tab))
        self.file_menu.add_command(label="Open", command=lambda : self.open_file(self.current_tab))
        self.file_menu.add_command(label="Save", command=lambda : self.save_file(self.current_tab))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)

        self.menu.add_cascade(label="File", menu=self.file_menu)

        """Menu for tabs"""
        self.menu.add_command(label='X', command=self.close_tab)

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
        self.parent_tabs.add(tab_w_box, text=tab_w_box.tab_name)
        tab_w_box.add_text_box()

        self.add_tab_scroll()
        # Implement scrolling if a large number of tabs is opened...

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
        tab_host.grid(column=0, row=0, sticky='NE')
        # Add a button.
        tab_host.bind('<Button-1>', self.new_tab)
        # Create new tab when pressing the new tab button.

    @log.log_function
    def add_tab_scroll(self):
        """
        Add scroll buttons to the parent_tabs notebook if there are too many
        tabs.
        """

        if len(self.parent_tabs.tabs()) >5:
            scroll_tab_l = tk.ttk.Button(self.panes, text='<')
            scroll_tab_l.grid(column=0, row=1, sticky='NE')
            scroll_tab_r = tk.ttk.Button(self.panes, text='>')
            scroll_tab_r.grid(column=1, row=1, sticky='NE')
            # Add scroll buttons.
            scroll_tab_l.bind('<Button-1>', self.scroll_tab_left)
            scroll_tab_r.bind('<Button-1>', self.scroll_tab_right)
            # Scroll to left or right tab.


    def scroll_tab_left(self, event):
        """
        Select tab to the left.
        """
        first_tab = self.parent_tabs.tabs()[0]
        all_tabs = self.parent_tabs.tabs()
        # Get ID of first and last tabs.

        if self.parent_tabs.index(self.current_tab) != 0:
            # If we're not at the first tab, scroll left.

            index_now = self.parent_tabs.index(self.current_tab)
            left_index = index_now-1
            # Get index of tab to the left.
            next_left = self.parent_tabs.tabs()[left_index]
            self.parent_tabs.select(next_left)
            # Get widget name of tab to the left and switch to it.

            tabs_to_end = index_now+13

            # Hide some tabs:
            for t in all_tabs[tabs_to_end:]:
                self.parent_tabs.hide(t)
            self.parent_tabs.add(all_tabs[left_index-1])
             # Add tab two to the left.

        else:
            pass

    def scroll_tab_right(self, event):
        """
        Select tab to the right.
        """
        all_tabs = self.parent_tabs.tabs()
        last_tab = self.parent_tabs.tabs()[-1]
        # Get ID of first and last tabs.

        if self.parent_tabs.index(self.current_tab) != len(all_tabs):
            # If we're not at the last tab, scroll right.

            index_now = self.parent_tabs.index(self.current_tab)
            right_index = index_now+1
            # Get index of tab to the left.
            next_right = self.parent_tabs.tabs()[right_index]
            self.parent_tabs.select(next_right)
            # Get widget name of tab to the left and switch to it.

            tabs_to_end = index_now

            # Hide some tabs:
            for t in all_tabs[:tabs_to_end]:
                self.parent_tabs.hide(t)
        else:
            pass

    @log.log_function
    def close_tab(self):
        """
        Close selected tab.
        """
        self.parent_tabs.forget(self.current_tab)
