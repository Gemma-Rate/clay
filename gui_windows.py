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

    def __init__(self, parent):
        tk.Tk.__init__(self, parent)
        self.parent = parent
        self.tag_colors = {''}

        self.current_tab = None
        self.tab_no = None
        # Empty attributes to fill later.

        self.tab_size = 15
        # Number of letters in tab size.

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
        self.parent_tabs.grid(row=0, column=0, columnspan=4, sticky='EW')

        # Add tab:
        self.new_tab()
        # Make a text box with this tab.
        self.tab_add_close_button()
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

        self.parent_tabs.tab(tab, text=self.new_tab_text_length(file))
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
            tab.raw = data
            # Raw text.

        self.parent_tabs.tab(tab, text=self.new_tab_text_length(file))
        # Change tab name to loaded file name.

    @log.log_function
    def new_file(self, tab):
        """
        Check if the current file should be saved,
        then create a new file.
        """
        self.save_file(tab)
        tab.text.delete("1.0", tk.END)

        default_tab_name = 'Document '+str(len(self.parent_tabs.tabs()))
        default_tab_name = self.new_tab_text_length(default_tab_name)
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

        self.config(menu=self.menu)

        """Menu for highlights"""
        self.highlight_menu = tk.Menu(self.menu)

        toggle_list = ['Adjective', 'Verb']
        # List of toggle highlight names.
        self.to_toggle = [('RB', 'RBR','RBS'), ('VB', 'VBD', 'VBG',
                           'VBN', 'VBP', 'VBZ')]
        # List of word tag groups corresponding to toggle_list names.
        self.set_to_on = [tk.IntVar(value=1) for x in toggle_list]

        for tl, stt, tg in zip(toggle_list, self.to_toggle, self.set_to_on):
            # Start by setting all selections to on.
            self.highlight_menu.add_checkbutton(label=tl, onvalue=1,
                                                offvalue=0,
                                                command=lambda : self.highlight_checkbox_control(stt),
                                                variable=tg)
            # Add menu checkbox for each type of word highlight.

        self.menu.add_cascade(label='Highlights', menu=self.highlight_menu)

        """Menu for tabs:"""
        self.menu.add_command(label='H', command=self.highlight)
        self.menu.add_command(label='R', command=self.remove_formatting)


    @log.log_function
    def new_tab(self, event=None):
        """
        Add a new text box tab.
        """
        self.stop_width()

        default_tab_name = 'Document '+str(len(self.parent_tabs.tabs()))
        default_tab_name = self.new_tab_text_length(default_tab_name)
        # Ensure tabs are consistent length.

        tab_w_box = tb.TabTextBox(self.parent_tabs, self.master_height,
                                  self.master_width, default_tab_name)
        # Internal container class.
        self.parent_tabs.add(tab_w_box, text=tab_w_box.tab_name)
        tab_w_box.add_text_box()

        return tab_w_box

    @log.log_function
    def new_tab_text_length(self, tab_text):
        """
        Ensure tab title text is the same length as the number defined in
        self.tab_size.
        """
        if '/' in tab_text:
            # Search for file path.
            splitted = tab_text.split('/')
            tab_text = splitted[-1]
            # Take last element (likely to be file name).

        list_of_numbers = list(range(1, self.tab_size))
        # Numbers 1 to self.tab_size.

        max_size = self.tab_size-3
        new_str = ''
        for i,t in zip(list_of_numbers, tab_text):
            if i < max_size:
                new_str += t
            else:
                new_str += '.'
                # If tab string is oversized, add ...

        if len(new_str) < self.tab_size:
            # If tab string is undersized, add spaces.
            spaces_to_add = self.tab_size-len(new_str)
            new_str += spaces_to_add*' '

        return new_str

    @log.log_function
    def select_tab_type(self, event):
        """
        Select tab class based on currently selected tab.
        """
        current_tab_name = self.parent_tabs.select()
        self.current_tab = self.parent_tabs.nametowidget(current_tab_name)
        # Get current tab (for open/closing functions).

    @log.log_function
    def tab_add_close_button(self):
        """
        Button for generating new tabs.
        """
        tab_add = tk.ttk.Button(self.panes, text='+', width=2)
        tab_add.grid(column=3, row=1, sticky='NE')
        # Add a button to open a new tab.
        tab_add.bind('<Button-1>', self.new_tab)
        # Create new tab when pressing the new tab button.

        tab_close = tk.ttk.Button(self.panes, text='x', width=2)
        tab_close.grid(column=0, row=1, sticky='NE')
        tab_close.bind('<Button-1>', self.close_tab)

    @log.log_function
    def add_tab_scroll(self):
        """
        Add scroll buttons to the parent_tabs notebook if there are too many
        tabs.
        """

        scroll_tab_l = tk.ttk.Button(self.panes, text='<', width=2)
        scroll_tab_l.grid(column=1, row=1, sticky='NE')
        scroll_tab_r = tk.ttk.Button(self.panes, text='>', width=2)
        scroll_tab_r.grid(column=2, row=1, sticky='NE')
        # Add scroll buttons.
        scroll_tab_l.bind('<Button-1>', self.scroll_tab_left)
        scroll_tab_r.bind('<Button-1>', self.scroll_tab_right)
        # Scroll to left or right tab.

    @log.log_function
    def scroll_tab_left(self, event=None):
        """
        Select tab to the left.
        """
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

            tabs_to_end = index_now+6

            # Hide some tabs:
            for t in all_tabs[tabs_to_end:]:
                self.parent_tabs.hide(t)
            self.parent_tabs.add(all_tabs[left_index-1])
             # Add tab two to the left.

        else:
            pass

    @log.log_function
    def scroll_tab_right(self, event=None):
        """
        Select tab to the right.
        """
        all_tabs = self.parent_tabs.tabs()
        # Get ID of all tabs.
        tot_index = len(all_tabs)-1
        # Total index to compare.

        if self.parent_tabs.index(self.current_tab) != tot_index:
            # If we're not at the last tab, scroll right.

            index_now = self.parent_tabs.index(self.current_tab)
            right_index = index_now+1
            # Get index of tab to the left.

            next_right = self.parent_tabs.tabs()[right_index]
            self.parent_tabs.select(next_right)
            # Get widget name of tab to the right and switch to it.

            tabs_to_end = index_now

            # Hide some tabs:
            for t in all_tabs[:tabs_to_end]:
                self.parent_tabs.hide(t)
        else:
            pass

    @log.log_function
    def close_tab(self, event):
        """
        Close selected tab.
        """
        self.parent_tabs.forget(self.current_tab)

    @log.log_function
    def stop_width(self):
        """
        Stop extra tabs from expanding the widths beyond the window.
        """
        number_of_tabs = len(self.parent_tabs.tabs())+1

        if number_of_tabs >= 8:
            self.add_tab_scroll()
            # Implement scrolling if a large number of tabs is opened...
            self.scroll_tab_right()
            # Scroll left to make room for the new tab.

    @log.log_function
    def highlight(self):
        """
        Wrapper to highlight words in a text box of a tab.
        """
        self.current_tab.highlight_word_types(self.to_toggle)

    @log.log_function
    def remove_formatting(self):
        """
        Remove formatting from text in a tab (e.g highlights).
        """
        self.current_tab.text.delete('1.0', 'end-1c')
        self.current_tab.text.insert(tk.END, self.current_tab.raw)


    @log.log_function
    def highlight_checkbox_control(self, word_class_list):
        """
        Create checkboxes to select the classes of word types to highlight.
        """
        if word_class_list not in self.to_toggle:
            self.to_toggle.append(word_class_list)
        else:
            self.to_toggle.remove(word_class_list)


